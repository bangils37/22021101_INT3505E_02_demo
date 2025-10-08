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

3.  **Chạy Frontend (tùy chọn, để kiểm tra API):**

    ```bash
    python week_04/front-end/app.py
    ```

## Điểm cuối API (v4)

URL cơ sở: `http://127.0.0.1:5000/api/v4`

### Sách

*   **GET /books**: Lấy danh sách sách.
*   **GET /books/{book_id}**: Lấy sách theo ID.
*   **POST /books**: Tạo sách mới.
*   **PUT /books/{book_id}**: Cập nhật sách.
*   **DELETE /books/{book_id}**: Xóa sách.

### Mượn/Trả

*   **GET /borrows**: Lấy danh sách mượn/trả.
*   **GET /borrows/{borrow_id}**: Lấy mượn/trả theo ID.
*   **POST /borrows**: Tạo bản ghi mượn/trả mới.
*   **PUT /borrows/{borrow_id}**: Cập nhật bản ghi mượn/trả.
*   **DELETE /borrows/{borrow_id}**: Xóa bản ghi mượn/trả.

## Tài liệu API

Xem Swagger UI tại: `http://127.0.0.1:5000/api/docs`