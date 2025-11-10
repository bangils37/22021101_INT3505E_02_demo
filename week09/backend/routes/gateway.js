'use strict';

const express = require('express');
const router = express.Router();
const store = require('../lib/store');
const { problem, sendProblem } = require('../lib/problem');

function resolveVersion(req) {
  const header = req.get('X-API-Version');
  const query = req.query.version;
  const v = parseInt(header || query || '1', 10);
  return Number.isNaN(v) ? 1 : v;
}

// POST /api/payments — routes to v1 or v2 based on version
router.post('/payments', (req, res) => {
  const v = resolveVersion(req);
  if (v === 2) {
    try {
      const idempotencyKey = req.get('Idempotency-Key');
      const payment = store.createPaymentV2(req.body, idempotencyKey);
      return res.status(201).json(payment);
    } catch (err) {
      const prob = problem({
        type: 'https://example.com/problems/validation-error',
        title: err.title || 'Invalid request',
        status: err.status || 400,
        detail: err.detail || 'Invalid payload',
      });
      return sendProblem(res, prob);
    }
  }
  // v1 default
  try {
    const payment = store.createPaymentV1(req.body);
    return res.status(201).json(payment);
  } catch (err) {
    const code = err.code || 400;
    return res.status(code).json({ error: err.error || 'Bad request' });
  }
});

// GET /api/payments/:id — returns according to version (only error format differs)
router.get('/payments/:id', (req, res) => {
  const v = resolveVersion(req);
  const payment = store.getPayment(req.params.id);
  if (!payment) {
    if (v === 2) {
      const prob = problem({
        type: 'https://example.com/problems/not-found',
        title: 'Payment not found',
        status: 404
      });
      return sendProblem(res, prob);
    }
    return res.status(404).json({ error: 'Not found' });
  }
  res.json(payment);
});

// POST /api/payments/:id/refund — only available in v1
router.post('/payments/:id/refund', (req, res) => {
  const v = resolveVersion(req);
  if (v === 2) {
    const prob = problem({
      type: 'https://example.com/problems/not-supported',
      title: 'Refund endpoint moved/changed in v2',
      status: 404,
      detail: 'Use the v2 workflow for refunds (not implemented in this demo)'
    });
    return sendProblem(res, prob);
  }
  const refund = store.refundPaymentV1(req.params.id);
  if (!refund) return res.status(404).json({ error: 'Payment not found' });
  res.json(refund);
});

module.exports = router;