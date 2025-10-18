## Tính năng

-   Đăng ký người dùng mới (`/register`)
-   Đăng nhập người dùng và nhận `accessToken` (`/login`)
-   Truy cập tuyến đường được bảo vệ (`/books`) chỉ với token hợp lệ

## Cài đặt và Chạy

1.  **Cài đặt các gói cần thiết:**

    ```bash
    npm install
    ```

2.  **Tạo tệp `.env`:**

    Tạo tệp `.env` ở thư mục gốc với nội dung sau:

    ```
    JWT_SECRET=supersecretkey
    PORT=5000
    ```

3.  **Chạy máy chủ:**

    ```bash
    node server.js
    ```

    Máy chủ sẽ chạy tại `http://localhost:5000`.

## Các Endpoint API

-   **`POST /register`**: Đăng ký người dùng.
    -   **Yêu cầu:** `{"username": "testuser", "password": "testpassword"}`
    -   **Phản hồi:** `User registered successfully.` (201)

-   **`POST /login`**: Đăng nhập và nhận token.
    -   **Yêu cầu:** `{"username": "testuser", "password": "testpassword"}`
    -   **Phản hồi:** `{"accessToken": "<token_của_bạn>"}`

-   **`GET /books`**: Lấy danh sách sách (cần token).
    -   **Header:** `Authorization: Bearer <token_của_bạn>`
    -   **Phản hồi:** Danh sách sách (200 OK) hoặc lỗi (401/403).

## Kiểm tra cơ bản

-   **Token hợp lệ:** 200 OK
-   **Token sai:** 403 Forbidden
-   **Token hết hạn:** 401 Unauthorized
-   **Token không bị ghi log:** Kiểm tra console máy chủ.

## Kiểm tra tự động (Python)

Để chạy script kiểm tra tự động `test.py`:

1.  **Cài đặt thư viện Python:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Chạy script kiểm tra:**

    ```bash
    python test.py
    ```

    Script này sẽ tự động đăng ký người dùng, đăng nhập, lấy token và kiểm tra truy cập vào endpoint `/books`.