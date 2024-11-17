const config = {
    SCRIPT_ID: 'arosualdata', // From script's URL
    DEPLOYMENT_ID: 'AKfycbzkJuMIyWcZ7DAg9bhHY770K4YhMAWKHASBtXl9kn8MpF3mu38DAb8d_8axcfuGSB8g', // From deployment settings
    BASE_URL: 'https://script.google.com/macros/s/AKfycbzkJuMIyWcZ7DAg9bhHY770K4YhMAWKHASBtXl9kn8MpF3mu38DAb8d_8axcfuGSB8g/exec',
    IPINFO_TOKEN: '6ef0f26335447e',
    MORPHCAST_LICENSE: 'sk9bebf5467e79a53a382ee56f1293c7e03b406b94f0af'
};

// Construct the full URL
config.GOOGLE_SCRIPT_URL = `${config.BASE_URL}${config.SCRIPT_ID}/exec`;
// Or with deployment ID
config.GOOGLE_SCRIPT_DEPLOYMENT_URL = `${config.BASE_URL}AKfycbz${config.DEPLOYMENT_ID}/exec`;

export default config;
