// src/models/userModel.js
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const pool = require('../config/dbConfig');
require('dotenv').config();  // Load environment variables from .env

// Create a new user
const createUser = async (email, password, firstName, lastName) => {
  const hashedPassword = await bcrypt.hash(password, 10);  // Hash the password
  try {
    const result = await pool.query(
      'INSERT INTO users (email, hashed_password, first_name, last_name) VALUES ($1, $2, $3, $4) RETURNING *',
      [email, hashedPassword, firstName, lastName]
    );
    return result.rows[0];  // Return the created user
  } catch (err) {
    console.error('Error creating user:', err);
    throw err;  // Rethrow error for the controller to handle
  }
};

// Get user by email
const getUserByEmail = async (email) => {
  try {
    const result = await pool.query('SELECT * FROM users WHERE email = $1', [email]);
    return result.rows[0];  // Return user or undefined if not found
  } catch (err) {
    console.error('Error fetching user by email:', err);
    throw err;
  }
};

// Generate JWT token
const generateToken = (userId) => {
  const secret = process.env.JWT_SECRET;  // Get the secret from .env file

  if (!secret) {
    throw new Error('JWT_SECRET is not defined in the .env file');  // Ensure secret is defined
  }

  return jwt.sign({ userId }, secret, { expiresIn: '1h' });  // Generate JWT with 1-hour expiry
};

module.exports = { createUser, getUserByEmail, generateToken };
