# Week08 - Postman/Newman Test Suite

Nội dung bổ sung so với `week07`:

- Thêm Postman collection (`postman/collection.json`) và environment (`postman/env.json`) cho 5 endpoints:
  - `GET /products`
  - `POST /products`
  - `GET /products/{id}`
  - `PUT /products/{id}`
  - `DELETE /products/{id}`
- Thêm script chạy test tự động bằng Newman.

## Cách chạy

1. Cài đặt dependencies trong backend:

```bash
cd week08/backend
npm install
```

2. Chạy test tự động (script sẽ tự khởi động server và chạy Newman):

```bash
npm run test:api
```

Kết quả report JSON sẽ được xuất ra: `week08/postman/reports/report.json`.

> Lưu ý: Server chạy ở `http://localhost:8080` (theo `backend/index.js`).