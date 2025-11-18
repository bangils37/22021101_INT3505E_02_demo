# Tuần 10: Demo Vận hành Dịch vụ – Bảo mật & Giám sát

Dự án demo này minh họa các khái niệm về Vận hành Dịch vụ, tập trung vào Bảo mật và Giám sát cho một API.

## Các tính năng chính:

1.  **Ghi nhật ký (Logging) với Winston**: Triển khai ghi nhật ký cơ bản ra console và vào các tệp (`error.log` cho lỗi, `combined.log` cho tất cả các nhật ký).
2.  **Giám sát (Monitoring) với Prometheus**: Cung cấp một endpoint `/metrics` để Prometheus thu thập dữ liệu, cung cấp các chỉ số mặc định của Node.js và các chỉ số tùy chỉnh về thời lượng yêu cầu HTTP.
3.  **Giới hạn tốc độ (Rate Limiting) với express-rate-limit**: Bảo vệ các endpoint API khỏi việc lạm dụng bằng cách giới hạn số lượng yêu cầu từ một địa chỉ IP duy nhất trong một khoảng thời gian nhất định.

## Cách chạy:

1.  Điều hướng đến thư mục `week10/backend`:
    ```bash
    cd week10/backend
    ```
2.  Cài đặt các phụ thuộc:
    ```bash
    npm install
    ```
3.  Khởi động ứng dụng:
    ```bash
    node index.js
    ```

    API sẽ chạy trên `http://localhost:3000`.

## Các Endpoint:

-   `GET /`: Một endpoint cơ bản.
-   `GET /data`: Một endpoint trả về một số dữ liệu JSON.
-   `GET /metrics`: Hiển thị các chỉ số Prometheus.

## Kiểm tra Giới hạn tốc độ:

Truy cập liên tục `http://localhost:3000/` hoặc `http://localhost:3000/data`. Sau 100 yêu cầu trong vòng 15 phút từ cùng một IP, bạn sẽ nhận được thông báo "Too many requests" (Quá nhiều yêu cầu).