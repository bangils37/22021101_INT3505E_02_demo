const express = require('express');
const winston = require('winston');
const client = require('prom-client');
const rateLimit = require('express-rate-limit');

const app = express();
const port = 3000;

// 1. Logging with Winston
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.json(),
    defaultMeta: { service: 'user-service' },
    transports: [
        new winston.transports.Console(),
        new winston.transports.File({ filename: 'error.log', level: 'error' }),
        new winston.transports.File({ filename: 'combined.log' }),
    ],
});

app.use((req, res, next) => {
    logger.info(`Request received: ${req.method} ${req.url}`);
    next();
});

// 2. Monitoring with Prometheus
const collectDefaultMetrics = client.collectDefaultMetrics;
collectDefaultMetrics({ register: client.register });

const httpRequestDurationMicroseconds = new client.Histogram({
    name: 'http_request_duration_ms',
    help: 'Duration of HTTP requests in ms',
    labelNames: ['method', 'route', 'code'],
    buckets: [50, 100, 200, 400, 800, 1600, 3200, 6400]
});

app.use((req, res, next) => {
    const end = httpRequestDurationMicroseconds.startTimer();
    res.on('finish', () => {
        end({ method: req.method, route: req.route ? req.route.path : req.url, code: res.statusCode });
    });
    next();
});

app.get('/metrics', async (req, res) => {
    res.set('Content-Type', client.register.contentType);
    res.end(await client.register.metrics());
});

// 3. Rate Limiting
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // Limit each IP to 100 requests per windowMs
    message: 'Too many requests from this IP, please try again after 15 minutes',
});

app.use(limiter);

// Routes
app.get('/', (req, res) => {
    logger.info('Root endpoint accessed');
    res.send('Hello World! This is a secure and monitored API.');
});

app.get('/data', (req, res) => {
    logger.info('Data endpoint accessed');
    res.json({ message: 'Some sensitive data' });
});

app.listen(port, () => {
    logger.info(`App listening at http://localhost:${port}`);
    console.log(`App listening at http://localhost:${port}`);
});