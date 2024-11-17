# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Emotion Tracking Analysis",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Google Sheets Connection
@st.cache_resource
def get_google_sheets_connection():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    service = build('sheets', 'v4', credentials=credentials)
    return service

def save_to_sheets(data, sheet_service):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Extract data
    emotion_data = [item for item in data.get('trackingData', [])
                   if item['type'] == 'FACE_EMOTION']
    attention_data = [item for item in data.get('trackingData', [])
                     if item['type'] == 'FACE_ATTENTION']
    geo_data = next((item['geoData'] for item in data.get('trackingData', [])
                    if item['type'] == "GEO_INFO"), {})
    
    # Calculate metrics
    avg_attention = np.mean([item.get('attention', 0) for item in attention_data]) if attention_data else 0
    emotion_counts = {}
    for item in emotion_data:
        emotion = item.get('dominantEmotion')
        if emotion:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else 'Unknown'

    # Prepare row data
    row_data = [[
        timestamp,
        data.get('deviceDetails', {}).get('browser', 'N/A'),
        data.get('deviceDetails', {}).get('platform', 'N/A'),
        geo_data.get('country', 'N/A'),
        geo_data.get('city', 'N/A'),
        avg_attention,
        dominant_emotion,
        json.dumps(emotion_counts),
        json.dumps(data.get('trackingData', []))
    ]]
    
    sheet_service.spreadsheets().values().append(
        spreadsheetId=st.secrets["spreadsheet_id"],
        range='Sheet1!A:I',
        valueInputOption='RAW',
        body={'values': row_data}
    ).execute()

def process_emotion_data(emotion_data):
    if not emotion_data:
        return pd.DataFrame()
    
    processed_data = []
    for item in emotion_data:
        if 'mediaTime' in item and 'emotions' in item:
            emotions = item['emotions']
            emotions['mediaTime'] = item['mediaTime']
            processed_data.append(emotions)
    
    return pd.DataFrame(processed_data)

def create_emotion_plot(df):
    if df.empty:
        return None
    
    emotion_cols = [col for col in df.columns if col != 'mediaTime']
    melted_df = df.melt(id_vars=['mediaTime'], 
                       value_vars=emotion_cols,
                       var_name='Emotion', 
                       value_name='Intensity')
    
    fig = px.line(melted_df, 
                  x='mediaTime', 
                  y='Intensity',
                  color='Emotion',
                  title='Emotion Intensity Over Time')
    fig.update_layout(
        xaxis_title="Video Timeline (seconds)",
        yaxis_title="Emotion Intensity",
        hovermode='x unified'
    )
    return fig

def main():
    st.title("🎭 Emotion Tracking Analysis")
    st.markdown("""
    Upload your emotion tracking JSON file to analyze and store the results.
    The data will be processed and stored in a Google Sheet for further analysis.
    """)
    
    uploaded_file = st.file_uploader(
        "Upload emotion tracking JSON file",
        type=['json'],
        help="Upload the JSON file generated from emotion tracking"
    )
    
    if uploaded_file:
        try:
            data = json.load(uploaded_file)
            
            # Layout
            device_col, geo_col = st.columns(2)
            
            with device_col:
                st.subheader("📱 Device Information")
                device_info = data.get('deviceDetails', {})
                st.json(device_info)
            
            with geo_col:
                st.subheader("📍 Location Information")
                geo_data = next((item['geoData'] for item in data.get('trackingData', [])
                               if item['type'] == "GEO_INFO"), {})
                st.json(geo_data)
            
            # Emotion Analysis
            st.subheader("😊 Emotion Analysis")
            emotion_data = [item for item in data.get('trackingData', [])
                          if item['type'] == 'FACE_EMOTION']
            
            if emotion_data:
                df = process_emotion_data(emotion_data)
                if not df.empty:
                    fig = create_emotion_plot(df)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Summary metrics
                        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                        
                        with metrics_col1:
                            dominant_emotions = df.drop('mediaTime', axis=1).idxmax(axis=1).value_counts()
                            st.metric("Most Frequent Emotion", dominant_emotions.index[0])
                            
                        with metrics_col2:
                            avg_intensity = df.drop('mediaTime', axis=1).mean().max()
                            st.metric("Highest Average Intensity", f"{avg_intensity:.2f}")
                            
                        with metrics_col3:
                            emotion_changes = df.drop('mediaTime', axis=1).idxmax(axis=1).nunique()
                            st.metric("Number of Emotion Changes", emotion_changes)
            
            # Upload button
            st.markdown("---")
            if st.button("📤 Upload to Database", type="primary"):
                with st.spinner("Uploading data..."):
                    try:
                        sheet_service = get_google_sheets_connection()
                        save_to_sheets(data, sheet_service)
                        st.success("✅ Data successfully uploaded!")
                        
                        # Show confirmation details
                        st.info(f"""
                        Upload Summary:
                        - Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                        - Location: {geo_data.get('city', 'N/A')}, {geo_data.get('country', 'N/A')}
                        - Device: {device_info.get('platform', 'N/A')}
                        """)
                    except Exception as e:
                        st.error(f"❌ Error uploading data: {str(e)}")
                        st.error("Please check your Google Sheets connection and try again.")
        
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON file. Please upload a valid JSON file.")
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            st.error("Please ensure the file format matches the expected structure.")

if __name__ == "__main__":
    main()
