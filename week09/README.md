# Week09 - API Versioning Case Study & Deprecation Notice

Nội dung tuần này tập trung vào case study nâng cấp API thanh toán từ v1 → v2, thực hành viết deprecation notice và lập kế hoạch migration.

## Nội dung chính
- Case study: Chiến lược nâng cấp v1 → v2 cho Payment API.
- Deprecation notice: Thông báo, timeline, header theo chuẩn, và hướng dẫn migration.
- OpenAPI mẫu cho v1/v2 để minh họa breaking changes.
- Migration plan và checklist triển khai.

## Cấu trúc
- `docs/strategy.md` — Chiến lược nâng cấp chi tiết.
- `docs/deprecation-notice.md` — Mẫu thông báo deprecation cho developers.
- `docs/migration-plan.md` — Kế hoạch migration theo từng giai đoạn.
- `openapi/v1.yaml` — API v1 (hiện trạng).
- `openapi/v2.yaml` — API v2 (đề xuất thiết kế mới).

## Chạy demo backend

```bash
cd week09/backend
npm start
```

Server chạy ở `http://localhost:8081`.

### v1 (URL versioning, có deprecation headers)
- Tạo thanh toán:
  - `POST http://localhost:8081/api/v1/payments`
  - Body: `{ "amount": 129900, "currency": "USD", "payment_method": "card_tok_abc123" }`
- Lấy theo ID: `GET http://localhost:8081/api/v1/payments/{id}`
- Refund: `POST http://localhost:8081/api/v1/payments/{id}/refund`

### v2 (URL versioning, bắt buộc Idempotency-Key)
- Tạo thanh toán:
  - `POST http://localhost:8081/api/v2/payments`
  - Header: `Idempotency-Key: <unique-key>`
  - Body: `{ "amount": { "value": 1299.00, "currency": "USD" }, "paymentMethod": "card_tok_abc123" }`
- Lấy theo ID: `GET http://localhost:8081/api/v2/payments/{id}`

### Gateway (Header/Query versioning)
- `POST http://localhost:8081/api/payments` với:
  - Header `X-API-Version: 2` (hoặc query `?version=2`) → xử lý theo v2.
  - Không có header/query → mặc định v1.