## Cách chạy

1.  **Cài đặt phụ thuộc:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Chạy Backend:**
    ```bash
    python -m week_04.back-end.app
    ```
    Truy cập tại `http://127.0.0.1:5000`.

## Thiết kế cơ sở dữ liệu

- **books**: Lưu trữ thông tin về sách.
  - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
  - `title` (TEXT NOT NULL)
  - `author` (TEXT NOT NULL)

- **users**: Lưu trữ thông tin về người dùng.
  - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
  - `name` (TEXT NOT NULL)

- **borrows**: Lưu trữ thông tin về các bản mượn sách.
  - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
  - `user_id` (INTEGER NOT NULL, FOREIGN KEY REFERENCES users(id))
  - `book_id` (INTEGER NOT NULL, FOREIGN KEY REFERENCES books(id))
  - `borrow_date` (TEXT NOT NULL)
  - `return_date` (TEXT)

## Các đầu API

Ứng dụng cung cấp các điểm cuối API sau:

### 1. Lấy danh sách sách

- **GET `/api/v1/books`**
  - **Mô tả**: Lấy danh sách tất cả các cuốn sách, hỗ trợ phân trang và lọc.
  - **Tham số truy vấn (Query Parameters)**:
    - `page` (integer, tùy chọn): Số trang (mặc định: 1).
    - `page_size` (integer, tùy chọn): Số lượng mục trên mỗi trang (mặc định: 10).
    - `title` (string, tùy chọn): Lọc sách theo tiêu đề (không phân biệt chữ hoa chữ thường, khớp một phần).
    - `author` (string, tùy chọn): Lọc sách theo tác giả (không phân biệt chữ hoa chữ thường, khớp một phần).
  - **Phản hồi thành công (200 OK)**:
    ```json
    {
      "success": true,
      "data": [
        {
          "id": 1,
          "title": "The Lord of the Rings",
          "author": "J.R.R. Tolkien"
        }
      ],
      "page": 1,
      "page_size": 10
    }
    ```

### 2. Lấy bản mượn của người dùng

- **GET `/api/v1/users/{id}/borrows`**
  - **Mô tả**: Lấy danh sách các bản mượn của một người dùng cụ thể.
  - **Tham số đường dẫn (Path Parameters)**:
    - `id` (integer, bắt buộc): ID của người dùng.
  - **Phản hồi thành công (200 OK)**:
    ```json
    {
      "success": true,
      "data": [
        {
          "id": 1,
          "title": "The Lord of the Rings",
          "author": "J.R.R. Tolkien",
          "borrow_date": "2023-01-01",
          "return_date": "2023-01-15"
        }
      ],
      "page": 1,
      "page_size": 10
    }
    ```
  - **Phản hồi lỗi (404 Not Found)**: Người dùng không tồn tại.

Xem Swagger UI tại: `http://127.0.0.1:5000/api/docs`