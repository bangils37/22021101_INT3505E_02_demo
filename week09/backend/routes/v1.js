'use strict';

const express = require('express');
const router = express.Router();
const store = require('../lib/store');

// POST /api/v1/payments — v1 payload, no idempotency
router.post('/payments', (req, res) => {
  try {
    const payment = store.createPaymentV1(req.body);
    // v1: trả 201 theo chuẩn, nhưng tuỳ hệ thống bạn có thể trả 200
    res.status(201).json(payment);
  } catch (err) {
    const code = err.code || 400;
    // v1: lỗi không theo RFC 7807, trả về JSON đơn giản
    res.status(code).json({ error: err.error || 'Bad request' });
  }
});

// GET /api/v1/payments/:id
router.get('/payments/:id', (req, res) => {
  const payment = store.getPayment(req.params.id);
  if (!payment) return res.status(404).json({ error: 'Not found' });
  res.json(payment);
});

// POST /api/v1/payments/:id/refund
router.post('/payments/:id/refund', (req, res) => {
  const refund = store.refundPaymentV1(req.params.id);
  if (!refund) return res.status(404).json({ error: 'Payment not found' });
  res.json(refund);
});

module.exports = router;