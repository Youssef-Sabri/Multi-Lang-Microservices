// src/dbInit.js
const pool = require('./dbConfig'); // Assuming you already have dbConfig.js for database connection

const createTables = async () => {
  const createUsersTable = `
    CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      email VARCHAR(255) UNIQUE NOT NULL,
      hashed_password VARCHAR(255) NOT NULL,
      first_name VARCHAR(255),
      last_name VARCHAR(255),
      created_at TIMESTAMP DEFAULT NOW(),
      updated_at TIMESTAMP DEFAULT NOW()
    );
  `;

  const createLogsTable = `
    CREATE TABLE IF NOT EXISTS logs (
      id SERIAL PRIMARY KEY,
      user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
      action VARCHAR(255),
      timestamp TIMESTAMP DEFAULT NOW()
    );
  `;

  try {
    console.log('Initializing database...');

    // Run the SQL commands to create the tables if they don't exist
    await pool.query(createUsersTable);
    await pool.query(createLogsTable);

    console.log('Tables created or already exist.');
  } catch (error) {
    console.error('Error initializing database:', error);
  }
};

// Run the function when the app starts
createTables();

module.exports = createTables;