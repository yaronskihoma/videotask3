import dotenv from 'dotenv';

// Load environment variables from .env file
dotenv.config();

const config = {
    SUPABASE_URL: process.env.SUPABASE_URL,
    SUPABASE_KEY: process.env.SUPABASE_KEY,
    MORPHCAST_LICENSE: process.env.MORPHCAST_LICENSE,
    IPINFO_TOKEN: process.env.IPINFO_TOKEN,
    COMPLETION_CODE: process.env.COMPLETION_CODE,
    TASK_ID: process.env.TASK_ID,
};

export default config;
