'use strict';

const express = require('express');
const router = express.Router();
const store = require('../lib/store');
const { problem, sendProblem } = require('../lib/problem');

// POST /api/v2/payments — requires Idempotency-Key and v2 payload
router.post('/payments', (req, res) => {
  try {
    const idempotencyKey = req.get('Idempotency-Key');
    const payment = store.createPaymentV2(req.body, idempotencyKey);
    res.status(201).json(payment);
  } catch (err) {
    const prob = problem({
      type: 'https://example.com/problems/validation-error',
      title: err.title || 'Invalid request',
      status: err.status || 400,
      detail: err.detail || 'Invalid payload',
    });
    sendProblem(res, prob);
  }
});

// GET /api/v2/payments/:id — problem+json on 404
router.get('/payments/:id', (req, res) => {
  const payment = store.getPayment(req.params.id);
  if (!payment) {
    const prob = problem({
      type: 'https://example.com/problems/not-found',
      title: 'Payment not found',
      status: 404
    });
    return sendProblem(res, prob);
  }
  res.json(payment);
});

module.exports = router;