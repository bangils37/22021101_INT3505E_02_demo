'use strict';

const express = require('express');
const morgan = require('morgan');
const cors = require('cors');

const { deprecationHeaders } = require('./middleware/deprecation');
const v1Routes = require('./routes/v1');
const v2Routes = require('./routes/v2');
const gatewayRoutes = require('./routes/gateway');

const PORT = process.env.PORT || 8081;
const app = express();

app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

// Healthcheck
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Versioned URLs
app.use('/api/v1', deprecationHeaders({
  sunset: 'Wed, 12 Feb 2025 23:59:59 GMT',
  link: 'https://example.com/docs/api/v1-deprecation'
}), v1Routes);

app.use('/api/v2', v2Routes);

// Gateway route: choose version via header/query, maps under /api
app.use('/api', gatewayRoutes);

app.listen(PORT, () => {
  console.log(`Week09 Payment API demo listening on http://localhost:${PORT}`);
  console.log('v1: URL /api/v1/* (deprecation headers enabled)');
  console.log('v2: URL /api/v2/* (requires Idempotency-Key for POST /payments)');
  console.log('Gateway: /api/* with X-API-Version or ?version=2');
});