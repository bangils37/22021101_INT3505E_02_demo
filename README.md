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

## Các API Endpoints

Dưới đây là danh sách ngắn gọn các API endpoint có sẵn:

### Phiên bản 1 (v1)

*   **GET /api/v1/getbooks**: Lấy tất cả sách.
*   **GET /api/v1/getborrows**: Lấy tất cả các lượt mượn.

### Phiên bản 2 (v2)

*   **GET /api/v2/getbooks**: Lấy tất cả sách (không có session tracking).
*   **GET /api/v2/getborrows**: Lấy tất cả các lượt mượn (không có session tracking).

### Phiên bản 3 (v3)

*   **GET /api/v3/getbooks**: Lấy tất cả sách (có hỗ trợ ETag để caching).
*   **GET /api/v3/getborrows**: Lấy tất cả các lượt mượn (có hỗ trợ ETag để caching).

### Phiên bản 4 (v4)

*   **GET /api/v4/books**: Lấy tất cả sách (có hỗ trợ ETag để caching).
*   **GET /api/v4/borrows**: Lấy tất cả các lượt mượn (có hỗ trợ ETag để caching).