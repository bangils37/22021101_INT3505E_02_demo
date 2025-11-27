// server.js
const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const PORT = 3000;

// parse JSON body
app.use(bodyParser.json());

// endpoint webhook nhận sự kiện
app.post('/webhook', (req, res) => {
    const event = req.body.event;
    const message = req.body.message;

    console.log('--- Webhook received ---');
    console.log(`Event: ${event}`);
    console.log(`Message: ${message}`);

    // Thông báo cơ bản: console log
    console.log(`🔔 Thông báo: ${message}`);

    res.status(200).send('Webhook received');
});

app.listen(PORT, () => {
    console.log(`Webhook server listening at http://localhost:${PORT}/webhook`);
});