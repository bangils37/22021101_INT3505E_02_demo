# Chiến lược nâng cấp Payment API từ v1 → v2

## Mục tiêu
- Giảm nợ kỹ thuật, chuẩn hóa payload và lỗi theo chuẩn công nghiệp.
- Bổ sung tính năng: idempotency cho tạo thanh toán, trường số tiền linh hoạt, chuẩn lỗi RFC 7807.
- Đảm bảo backward compatibility trong giai đoạn chuyển đổi.

## Bối cảnh v1 (giả định)
- Endpoint: `/api/v1/payments` (POST tạo), `/api/v1/payments/{id}` (GET), `/api/v1/payments/{id}/refund` (POST).
- Body tạo dùng `amount` kiểu integer (cents), `currency` chuỗi 3 ký tự, `payment_method` dạng token.
- Không yêu cầu idempotency key; lỗi trả về không chuẩn hóa.

## Thiết kế v2 (đề xuất)
- Endpoint: `/api/v2/payments` (POST), `/api/v2/payments/{id}` (GET).
- Tính năng:
  - Bắt buộc header `Idempotency-Key` cho POST tạo thanh toán.
  - Chuẩn hóa số tiền: `amount: { value: number, currency: string }`.
  - Đổi tên trường camelCase: `paymentMethod` thay cho `payment_method`.
  - Chuẩn lỗi `application/problem+json` (RFC 7807) với trường `type`, `title`, `status`, `detail`, `traceId`.
- Trạng thái: `authorized`, `captured`, `refunded`, `failed`.

## Chiến lược versioning
- Chính: Version theo URL (`/api/v1/...` → `/api/v2/...`).
- Bổ trợ: Hỗ trợ header `X-API-Version: 1|2` và query `?version=2` qua gateway (nếu cần), ánh xạ sang đường dẫn v1/v2.
- Ưu tiên rõ ràng và dễ kiểm soát routing, logging, và metrics.

## Breaking changes quản lý thế nào
- Trường đổi tên (`payment_method` → `paymentMethod`) và cấu trúc `amount` mới.
- Bắt buộc `Idempotency-Key` ở v2.
- Lỗi chuẩn RFC 7807 thay thế lỗi tự do.
- Chính sách: v1 tiếp tục hoạt động trong thời gian song song (dual maintenance) 90 ngày trước khi sunset.

## Kế hoạch rollout (phased)
1. Chuẩn bị (T0):
   - Công bố v2, phát hành tài liệu, SDK beta, migration guide.
   - Bật v2 song song với v1; gateway định tuyến theo URL.
2. Dual maintenance (T0→T0+90):
   - Theo dõi metrics, lỗi, độ ổn định.
   - Cảnh báo deprecation qua headers (Deprecation/Sunset/Link) ở v1.
   - Cung cấp adaptor/gateway: chấp nhận `payment_method` và chuyển đổi sang `paymentMethod` nếu cần cho khách hàng lớn.
3. Cutover (T0+90):
   - Chặn tạo mới trên v1 (POST trả 410 Gone sau Sunset), chỉ cho phép GET trong thời gian ngắn.
   - Hoàn tất chuyển đổi lưu lượng sang v2.

## Routing & Compatibility
- API Gateway rules:
  - Nếu `X-API-Version=2` hoặc URL `/api/v2/*` → v2 service.
  - Nếu `X-API-Version=1` hoặc URL `/api/v1/*` → v1 service.
- Compat shim (tuỳ chọn): bộ chuyển đổi payload giúp khách hàng nâng cấp dần.

## Quan trắc và quản trị rủi ro
- Metrics: tỉ lệ lỗi, thời gian phản hồi, phần trăm traffic theo phiên bản.
- Logging: gắn `traceId`, lưu header `Idempotency-Key` để phát hiện retry.
- Rollback plan: sẵn sàng giảm lưu lượng về v1 nếu v2 bất ổn.

## Kiểm thử
- Contract tests: xác minh schema OpenAPI v1/v2.
- E2E: tạo, truy vấn, refund (nếu có), xử lý retry idempotent.
- Performance/regression: đảm bảo v2 không thoái hóa.

## Truyền thông
- Deprecation notice: email, Slack, banner trên docs, changelog.
- Headers: `Deprecation`, `Sunset`, `Link rel="deprecation"`, thông báo ở response body (nếu cần).
- Hỗ trợ: office hours, kênh support, ví dụ code.