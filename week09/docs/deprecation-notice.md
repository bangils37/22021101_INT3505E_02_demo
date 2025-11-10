# Deprecation Notice — Payment API v1

Xin chào developers,

Chúng tôi đã phát hành Payment API v2 với cải tiến về idempotency, chuẩn lỗi RFC 7807 và payload linh hoạt. Phiên bản v1 sẽ bước vào trạng thái deprecation theo timeline dưới đây.

## Timeline
- T0 (Thông báo): v2 sẵn sàng, v1 bắt đầu deprecation.
- T0 + 30 ngày: v1 trả thêm header cảnh báo deprecation cho tất cả requests.
- T0 + 90 ngày (Sunset): ngừng chấp nhận tạo thanh toán mới trên v1. Một số GET có thể duy trì thêm 30 ngày rồi ngừng hoàn toàn.

## Ảnh hưởng và thay đổi chính
- `payment_method` (v1) đổi thành `paymentMethod` (v2) theo camelCase.
- `amount` từ integer (cents) chuyển sang object `{ value, currency }`.
- POST tạo thanh toán yêu cầu header `Idempotency-Key` ở v2.
- Lỗi được chuẩn hóa theo `application/problem+json`.

## Headers deprecation (khuyến nghị)
Ví dụ đáp ứng v1 kèm theo header cảnh báo:
```
Deprecation: true
Sunset: Wed, 12 Feb 2025 23:59:59 GMT
Link: <https://example.com/docs/api/v1-deprecation>; rel="deprecation"; type="text/html"
```
- `Deprecation`: báo hiệu API v1 đang trong giai đoạn deprecation.
- `Sunset`: thời điểm ngừng cung cấp v1 theo RFC 8594.
- `Link` (rel=deprecation): trỏ tới tài liệu thông báo deprecation.

Body ví dụ (tuỳ chọn):
```json
{
  "deprecated": true,
  "sunset": "2025-02-12T23:59:59Z",
  "message": "v1 is deprecated. Please migrate to v2.",
  "migrationGuide": "https://example.com/docs/api/migration-to-v2"
}
```

## Hướng dẫn migration
- Thay đổi URL: `/api/v1/...` → `/api/v2/...`.
- Cập nhật body:
  - `payment_method` → `paymentMethod`.
  - `amount` integer → `amount.value` (number) + `amount.currency` (string).
- Thêm header `Idempotency-Key` (unique per create request) cho POST tạo thanh toán.
- Cập nhật parsing lỗi theo `application/problem+json`.

## Hỗ trợ
- Tài liệu v2: https://example.com/docs/api/v2
- Migration guide: https://example.com/docs/api/migration-to-v2
- Kênh hỗ trợ: support@example.com

Cảm ơn bạn đã đồng hành!