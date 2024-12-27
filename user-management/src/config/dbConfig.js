// src/config/dbConfig.js
const { Pool } = require('pg');
require('dotenv').config();  // Load environment variables from .env file

// Set up database connection using environment variables
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,  // Get database URL from the .env file
});

module.exports = pool;
