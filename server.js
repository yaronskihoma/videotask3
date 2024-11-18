const express = require('express');
const app = express();

const config = {
  SUPABASE_URL: process.env.SUPABASE_URL,
  SUPABASE_KEY: process.env.SUPABASE_KEY,
  MORPHCAST_LICENSE: process.env.MORPHCAST_LICENSE,
  IPINFO_TOKEN: process.env.IPINFO_TOKEN,
  COMPLETION_CODE: process.env.COMPLETION_CODE,
  TASK_ID: process.env.TASK_ID
};

app.get('/api/config', (req, res) => {
  res.json(config);
});

app.listen(3000, () => {
  console.log('Server listening on port 3000');
});
