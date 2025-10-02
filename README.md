# Demo Hệ thống Thư viện Đơn Giản - Week 03

## Mô tả

Đây là demo hệ thống quản lý thư viện đơn giản được xây dựng bằng Flask API theo yêu cầu SRS của buổi 3. Hệ thống cung cấp các chức năng cơ bản để quản lý sách và việc mượn trả sách.

## Cấu trúc Project

```
week_03/
├── app.py                               # Main Flask application
├── database.py                          # Database configuration & connection
├── routes/                              # API routes modules
│   ├── __init__.py                      # Routes package init
│   ├── books.py                         # Books management endpoints  
│   └── borrows.py                       # Borrowing management endpoints
├── requirements.txt                     # Python dependencies
├── README.md                           # Project documentation
├── test_api.py                         # API testing script
├── .gitignore                          # Git ignore rules
└── Library_API.postman_collection.json # Postman API collection
```

## Tính năng

### Quản lý sách (Books Module)
- ✅ [F1] Thêm sách mới
- ✅ [F2] Sửa thông tin sách  
- ✅ [F3] Xóa sách
- ✅ [F4] Lấy danh sách tất cả sách
- ✅ [F5] Lấy thông tin chi tiết của một sách

### Quản lý mượn trả (Borrow Module)  
- ✅ [F6] Mượn sách (giảm số lượng available)
- ✅ [F7] Trả sách (tăng số lượng available)
- ✅ [F8] Lấy danh sách các bản ghi mượn

## Kiến trúc

- **Framework**: Flask với Blueprint để tổ chức modules
- **Database**: SQLite với schema được định nghĩa trong `database.py`
- **API Style**: RESTful tuân thủ best practices
- **Data Format**: JSON responses với format chuẩn

## API Endpoints

### Books Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/books` | Lấy danh sách tất cả sách |
| POST | `/api/v1/books` | Thêm sách mới |
| GET | `/api/v1/books/{id}` | Lấy thông tin sách theo ID |
| PUT | `/api/v1/books/{id}` | Cập nhật thông tin sách |
| DELETE | `/api/v1/books/{id}` | Xóa sách |

### Borrowing Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/borrows` | Mượn sách |
| PUT | `/api/v1/borrows/{id}/return` | Trả sách |
| GET | `/api/v1/borrows` | Lấy danh sách bản ghi mượn |

## Cài đặt và Chạy

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Chạy ứng dụng

```bash
python app.py
```

Ứng dụng sẽ chạy tại: `http://localhost:5000`

### 3. Database

Database SQLite sẽ được tự động tạo với tên `library.db` khi chạy ứng dụng lần đầu.

## Ví dụ sử dụng API

### 1. Thêm sách mới

```bash
curl -X POST http://localhost:5000/api/v1/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "total_copies": 5
  }'
```

### 2. Lấy danh sách sách

```bash
curl -X GET http://localhost:5000/api/v1/books
```

### 3. Mượn sách

```bash
curl -X POST http://localhost:5000/api/v1/borrows \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "book_id": 1
  }'
```

### 4. Trả sách

```bash
curl -X PUT http://localhost:5000/api/v1/borrows/1/return
```

### 5. Lấy danh sách mượn

```bash
curl -X GET http://localhost:5000/api/v1/borrows
```

## Response Format

Tất cả API response đều tuân theo format chuẩn:

```json
{
  "success": true/false,
  "data": {...},
  "message": "Description message"
}
```

## Database Schema

### Books Table
```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    available_copies INTEGER NOT NULL DEFAULT 0,
    total_copies INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Borrows Table
```sql
CREATE TABLE borrows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    return_date TIMESTAMP NULL,
    status TEXT DEFAULT 'borrowed',
    FOREIGN KEY (book_id) REFERENCES books (id)
);
```

## Best Practices được áp dụng

1. **RESTful Design**: Sử dụng HTTP methods chuẩn và danh từ số nhiều cho endpoints
2. **API Versioning**: Sử dụng `/api/v1/` prefix
3. **Error Handling**: Response codes và messages rõ ràng
4. **Data Validation**: Kiểm tra input data
5. **Database Integrity**: Foreign key constraints và transaction handling
6. **Consistent Response Format**: JSON format thống nhất cho tất cả responses

## Tác giả

Demo được tạo cho môn INT3505E - Software Engineering

## License

This project is for educational purposes only.
