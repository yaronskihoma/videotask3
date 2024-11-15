# README.md
# Emotion Tracking Analysis

Web application for analyzing and storing emotion tracking data using Streamlit and Google Sheets.

## Setup
1. Create Google Cloud project and enable Sheets API
2. Create service account and download credentials
3. Create `.streamlit/secrets.toml` with credentials
4. Install dependencies: `pip install -r requirements.txt`
5. Run locally: `streamlit run app.py`

## Environment
- Python 3.8+
- Streamlit
- Google Sheets API
- Pandas

## Structure
```
emotion-tracking/
├── .gitignore
├── README.md
├── requirements.txt
├── app.py
└── .streamlit/
    └── secrets.toml
```

## Usage
1. Upload JSON from emotion tracking
2. Review analysis
3. Upload to database
