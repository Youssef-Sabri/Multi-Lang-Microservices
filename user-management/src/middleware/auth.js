// src/middleware/auth.js
const jwt = require('jsonwebtoken');
require('dotenv').config();  // Ensure the environment variables are loaded

const authenticateJWT = (req, res, next) => {
  const token = req.header('Authorization') && req.header('Authorization').split(' ')[1];  // Get the token (Bearer <token>)

  if (!token) {
    return res.status(401).send('Access denied');
  }

  const secret = process.env.JWT_SECRET;  // Get the secret from .env file

  jwt.verify(token, secret, (err, user) => {
    if (err) return res.status(403).send('Invalid token');  // Invalid token error
    req.user = user;  // Add the user info to the request
    next();  // Continue to the next middleware or route handler
  });
};

module.exports = authenticateJWT;
