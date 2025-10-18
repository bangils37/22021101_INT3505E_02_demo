require('dotenv').config();
const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

const app = express();
app.use(express.json());

const users = []; // In-memory user storage

// Register a new user
app.post('/register', async (req, res) => {
    try {
        const { username, password } = req.body;
        if (!username || !password) {
            return res.status(400).send('Username and password are required.');
        }

        const hashedPassword = await bcrypt.hash(password, 10);
        const user = { username, password: hashedPassword };
        users.push(user);
        res.status(201).send('User registered successfully.');
    } catch (error) {
        res.status(500).send('Error registering user.');
    }
});

// Login user and return JWT
app.post('/login', async (req, res) => {
    const { username, password } = req.body;
    const user = users.find(u => u.username === username);

    if (!user) {
        return res.status(400).send('Invalid credentials.');
    }

    try {
        if (await bcrypt.compare(password, user.password)) {
            const accessToken = jwt.sign({ username: user.username }, process.env.JWT_SECRET, { expiresIn: '15m' });
            res.json({ accessToken });
        } else {
            res.status(400).send('Invalid credentials.');
        }
    } catch (error) {
        res.status(500).send('Error logging in.');
    }
});

// Middleware to authenticate JWT
function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (token == null) return res.sendStatus(401); // No token

    jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
        if (err) {
            // S2: Token hết hạn -> 401 Unauthorized
            // S1: Token bị lộ (nếu in ra log) -> không in token ra log
            console.error('JWT verification error:', err.message); // Log error message, not the token
            return res.sendStatus(403); // Invalid token
        }
        req.user = user;
        next();
    });
}

// Protected route
app.get('/books', authenticateToken, (req, res) => {
    res.json([{ id: 1, title: 'Book 1' }, { id: 2, title: 'Book 2' }]);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});