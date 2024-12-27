require('dotenv').config();  // Load .env variables

const express = require('express');
const bodyParser = require('body-parser');
const userRoutes = require('./routes/userRoutes');
const createTables = require('./config/dbinit'); // Import the dbInit script

const app = express();

app.use(bodyParser.json());

// Use the user routes
app.use('/api/users', userRoutes);

const PORT = process.env.PORT || 3000;  // Default to 3000 if PORT is not set
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
