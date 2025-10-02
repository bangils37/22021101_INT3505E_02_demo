# 22021101_INT3505E_02_demo

## 📚 Demo Hệ thống Thư viện Đơn Giản - Week 03

Đây là repository demo cá nhân cho môn học **INT3505E** - Lớp 02, chứa bài tập **Week 03** về thiết kế API hệ thống thư viện đơn giản sử dụng Flask.

## 🗂️ Cấu trúc Repository

```
22021101_INT3505E_02_demo/
├── .git/                               # Git repository
├── .venv/                              # Python virtual environment  
├── .gitignore                          # Git ignore rules
├── README.md                           # Main project documentation
├── requirements.txt                    # Python dependencies (Flask, requests)
├── library.db                          # SQLite database (auto-generated)
└── week_03/                            # Week 03 - Library API Demo
    ├── app.py                          # Main Flask application  
    ├── database.py                     # Database models & initialization
    ├── routes/                         # Modular API routes
    │   ├── __init__.py                 # Routes package initializer
    │   ├── books.py                    # Books management endpoints
    │   └── borrows.py                  # Borrowing management endpoints
    ├── test_api.py                     # Automated API testing script
    ├── Library_API.postman_collection.json        # Postman collection  
    └── Simple_Library_API.postman_collection.json # Simple Postman collection
```

## 🎯 Mô tả Week 03

**Hệ thống Thư viện API** được xây dựng theo yêu cầu SRS buổi 3, tập trung vào:
- Thiết kế API RESTful tuân thủ best practices
- Quản lý sách và việc mượn trả
- Cấu trúc modular và có thể mở rộng

## ✅ Tính năng đã hoàn thành

### 📚 Quản lý sách (Books Module)
- ✅ **[F1]** Thêm sách mới - `POST /api/v1/books`
- ✅ **[F2]** Sửa thông tin sách - `PUT /api/v1/books/{id}`
- ✅ **[F3]** Xóa sách - `DELETE /api/v1/books/{id}`
- ✅ **[F4]** Lấy danh sách tất cả sách - `GET /api/v1/books`
- ✅ **[F5]** Lấy thông tin chi tiết một sách - `GET /api/v1/books/{id}`

### 📖 Quản lý mượn trả (Borrow Module)  
- ✅ **[F6]** Mượn sách (giảm available_copies) - `POST /api/v1/borrows`
- ✅ **[F7]** Trả sách (tăng available_copies) - `PUT /api/v1/borrows/{id}/return`
- ✅ **[F8]** Lấy danh sách bản ghi mượn - `GET /api/v1/borrows`

## 🏗️ Kiến trúc & Công nghệ

- **Framework**: Flask với Blueprint pattern
- **Database**: SQLite với auto-initialization  
- **API Design**: RESTful với chuẩn HTTP methods
- **Structure**: Modular routes trong folder riêng biệt
- **Testing**: Automated testing script + Postman collections
- **Environment**: Python virtual environment (.venv)

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

## 🚀 Cài đặt và Chạy

### Bước 1: Clone repository
```bash
git clone https://github.com/bangils37/22021101_INT3505E_02_demo.git
cd 22021101_INT3505E_02_demo
```

### Bước 2: Tạo virtual environment  
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

### Bước 3: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 4: Chạy ứng dụng
```bash
cd week_03
python app.py
```

**🌐 Server sẽ chạy tại**: `http://localhost:5000`

### Bước 5: Test API

#### Option 1: Automated Test Script
```bash
python test_api.py
```

#### Option 2: Import Postman Collection
- Mở Postman → Import → Chọn file `Library_API.postman_collection.json`
- Hoặc sử dụng `Simple_Library_API.postman_collection.json` cho version đơn giản hơn

### Bước 6: Xem Database
Database `library.db` sẽ được tự động tạo với dữ liệu mẫu gồm:
- **4 cuốn sách** (Clean Code, Design Patterns, Effective Python, Flask Web Development)  
- **3 bản ghi mượn** từ 2 users khác nhau

## 📋 Ví dụ sử dụng API

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

### 3. Lấy thông tin sách theo ID
```bash
curl -X GET http://localhost:5000/api/v1/books/1
```

### 4. Mượn sách
```bash
curl -X POST http://localhost:5000/api/v1/borrows \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "book_id": 1
  }'
```

### 5. Trả sách
```bash
curl -X PUT http://localhost:5000/api/v1/borrows/1/return
```

### 6. Lấy danh sách mượn (có filter)
```bash
# Tất cả bản ghi
curl -X GET http://localhost:5000/api/v1/borrows

# Theo user_id
curl -X GET "http://localhost:5000/api/v1/borrows?user_id=1"

# Theo status  
curl -X GET "http://localhost:5000/api/v1/borrows?status=borrowed"
```

## 📊 Database Schema & Sample Data

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

**Sample Data:**
- Clean Code by Robert C. Martin (Available: 3/5)
- Design Patterns by Gang of Four (Available: 2/3)  
- Effective Python by Brett Slatkin (Available: 4/4)
- Flask Web Development by Miguel Grinberg (Available: 1/2)

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

**Sample Data:**
- User 1 borrowed Book 1 (Clean Code) - Status: borrowed
- User 2 borrowed Book 2 (Design Patterns) - Status: borrowed  
- User 1 borrowed Book 4 (Flask Web Development) - Status: borrowed

## 🎯 Best Practices đã áp dụng

1. **🔗 RESTful API Design**
   - HTTP methods chuẩn (GET, POST, PUT, DELETE)
   - Endpoint naming với danh từ số nhiều
   - Status codes phù hợp (200, 201, 404, 400)

2. **📦 API Versioning**  
   - Sử dụng `/api/v1/` prefix cho tương lai mở rộng

3. **🏗️ Modular Architecture**
   - Tách routes thành modules riêng biệt
   - Blueprint pattern để tổ chức code

4. **🛡️ Error Handling**
   - Try-catch comprehensive 
   - Consistent error response format
   - Input validation

5. **💾 Database Best Practices**
   - Foreign key constraints
   - Auto-increment primary keys  
   - Timestamp tracking
   - Transaction handling

6. **🧪 Testing & Documentation**
   - Automated test script
   - Postman collections  
   - Clear API documentation
   - Sample data included

## 📈 Khả năng mở rộng

Hệ thống được thiết kế để dễ dàng mở rộng:
- ➕ Thêm User management module
- ➕ Authentication & Authorization
- ➕ Advanced search & filtering  
- ➕ Email notifications
- ➕ Book categories & tags
- ➕ Reservation system

## 🏆 Đánh giá SRS Requirements

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| **[N1]** Push lên private git repo | ✅ | Repository: `22021101_INT3505E_02_demo` |
| **[N2]** Best practices đặt tên endpoint | ✅ | RESTful naming conventions |  
| **[N3]** Dễ mở rộng | ✅ | Modular structure, Blueprint pattern |
| **[N4]** Response JSON rõ ràng | ✅ | Consistent format cho tất cả endpoints |
| **[F1-F8]** Đầy đủ 8 chức năng | ✅ | Tất cả endpoints hoạt động |

---

## 👨‍💻 Thông tin

- **Sinh viên**: [Your Name]
- **Mã số**: 22021101  
- **Lớp**: INT3505E_02
- **Buổi**: Week 03 - Thiết kế API
- **Framework**: Flask Python
- **Database**: SQLite

**🎯 Demo hoàn thành theo đúng yêu cầu SRS!**