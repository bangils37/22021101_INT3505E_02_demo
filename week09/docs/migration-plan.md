# Migration Plan — v1 → v2 Payment API

## Giai đoạn & Checklist

### Giai đoạn 1 — Chuẩn bị (T0)
- [ ] Hoàn tất OpenAPI v2, publish docs và SDK beta.
- [ ] Thiết lập routing v1/v2 theo URL, optional theo header/query.
- [ ] Bật logging `traceId` và theo dõi `Idempotency-Key` tại gateway.
- [ ] Viết deprecation notice, cập nhật banner trên docs.

### Giai đoạn 2 — Dual maintenance (T0→T0+90)
- [ ] Bật headers `Deprecation`, `Sunset`, `Link` cho v1 responses.
- [ ] Theo dõi metrics: lỗi, latency, tỷ lệ traffic v1/v2.
- [ ] Hỗ trợ adaptor chuyển `payment_method` → `paymentMethod` nếu cần.
- [ ] Chạy contract tests & E2E cho cả v1 & v2.

### Giai đoạn 3 — Cutover (T0+90)
- [ ] Chặn tạo thanh toán mới trên v1 (POST trả 410), giữ GET 30 ngày.
- [ ] Di chuyển hoàn toàn sang v2, hạ tầng v1 về chế độ đóng.
- [ ] Đánh giá hậu triển khai, cleanup tài liệu, thông báo hoàn tất.

## Bảng ánh xạ thay đổi
- URL: `/api/v1/payments` → `/api/v2/payments`.
- Body tạo:
  - `payment_method` → `paymentMethod` (camelCase).
  - `amount` integer → `amount.value` (number) + `amount.currency` (string).
- Header mới: `Idempotency-Key` bắt buộc ở v2 (POST tạo).
- Lỗi: từ JSON tự do → RFC 7807 (`application/problem+json`).

## Rủi ro & Giảm thiểu
- Risk: khách hàng chưa cập nhật →
  - Mitigation: adaptor tạm thời, windows dual maintenance, thông báo rõ ràng.
- Risk: sai lệch tính tiền do format mới →
  - Mitigation: test chuyển đổi, canary rollout, quan trắc chặt chẽ.