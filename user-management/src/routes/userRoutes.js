// src/routes/userRoutes.js
const express = require('express');
const bcrypt = require('bcryptjs');  // Add bcrypt import here
const { body, validationResult } = require('express-validator');
const { createUser, getUserByEmail, generateToken } = require('../models/userModel');
const authenticateJWT = require('../middleware/auth');
const router = express.Router();





// User registration route
router.post('/register',
  // Validate inputs
  body('email').isEmail().withMessage('Invalid email address'),
  body('password').isLength({ min: 6 }).withMessage('Password should be at least 6 characters'),
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const { email, password, firstName, lastName } = req.body;

    try {
      const existingUser = await getUserByEmail(email);
      if (existingUser) {
        return res.status(400).json({ error: 'User already exists' });
      }

      const user = await createUser(email, password, firstName, lastName);
      res.status(201).json({ message: 'User created successfully', userId: user.id });
    } catch (err) {
      res.status(500).json({ error: 'Error registering user' });
    }
  }
);

// User login route
router.post('/login',
    body('email').isEmail().withMessage('Invalid email address'),
    body('password').isLength({ min: 6 }).withMessage('Password should be at least 6 characters'),
    async (req, res) => {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }
  
      const { email, password } = req.body;
  
      try {
        const user = await getUserByEmail(email);  // Get the user from DB by email
        if (!user) {
          return res.status(400).json({ error: 'Invalid credentials' });  // User not found
        }
  
        const isPasswordValid = await bcrypt.compare(password, user.hashed_password);  // Compare hashed password
        if (!isPasswordValid) {
          return res.status(400).json({ error: 'Invalid credentials' });  // Invalid password
        }
  
        const token = generateToken(user.id);  // Generate JWT token
        res.json({ message: 'Login successful', token });  // Return success and token
      } catch (err) {
        console.error('Error during login:', err);  // Log any error
        res.status(500).json({ error: 'Error logging in user' });  // Handle error
      }
    }
  );
  

// Protected route
router.get('/protected', authenticateJWT, (req, res) => {
    res.send('This is a protected route');
  });
  

module.exports = router;
