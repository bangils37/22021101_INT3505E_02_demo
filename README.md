# Library Management API - Week 03

Flask API demo cho môn **INT3505E** - Hệ thống quản lý thư viện với các tính năng advanced.

## 🚀 Quick Start

```bash
# Clone và setup
git clone https://github.com/bangils37/22021101_INT3505E_02_demo.git
cd 22021101_INT3505E_02_demo
pip install -r requirements.txt

# Chạy server
cd week_03
python app.py

# Test API
python run_tests.py
```

**Server**: `http://localhost:5000`

## � Cấu trúc

```
week_03/
├── app.py                    # Flask app chính
├── database.py               # SQLite database
├── routes/                   # API endpoints
│   ├── books.py             # Quản lý sách  
│   └── borrows.py           # Quản lý mượn trả
├── tests/                    # Test suite
│   ├── test_api.py          # Basic tests
│   └── test_advanced_api.py # Advanced tests
└── run_tests.py             # Test runner
```

## ⚡ Tính năng

**Cơ bản:**
- ✅ CRUD sách (thêm, sửa, xóa, xem)
- ✅ Mượn/trả sách với tracking
- ✅ RESTful API design

**Advanced:**
- 🔥 **Pagination**: `?page=1&limit=10`
- 🔥 **Filtering**: `?author=Robert&status=available`
- 🔥 **Sorting**: `?sort=title&order=asc`

## �️ API Endpoints

### 📚 Books (5 endpoints)
```http
GET    /api/v1/books          # Danh sách + pagination/filter/sort
GET    /api/v1/books/1        # Chi tiết sách  
POST   /api/v1/books          # Thêm mới
PUT    /api/v1/books/1        # Cập nhật
DELETE /api/v1/books/1        # Xóa
```

### 📖 Borrows (3 endpoints) 
```http
GET    /api/v1/borrows        # Lịch sử + filter/sort
POST   /api/v1/borrows        # Mượn sách
PUT    /api/v1/borrows/1/return  # Trả sách
```

## 🔧 Advanced Features

### Pagination
```bash
GET /api/v1/books?page=2&limit=5&offset=10
```

### Filtering  
```bash
# Books
GET /api/v1/books?author=Robert&status=available

# Borrows  
GET /api/v1/borrows?user_id=1&status=borrowed
```

### Sorting
```bash
GET /api/v1/books?sort=title&order=desc
GET /api/v1/borrows?sort=borrow_date&order=asc
```

### Combined
```bash
GET /api/v1/books?author=Martin&sort=title&page=1&limit=3
```

## � Cài đặt

```bash
# Clone repo
git clone https://github.com/bangils37/22021101_INT3505E_02_demo.git
cd 22021101_INT3505E_02_demo

# Setup environment  
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
cd week_03
python app.py
```

**🌐 Server**: `http://localhost:5000`

## 🧪 Testing

```bash
# Run all tests
python run_tests.py

# Run specific tests  
python tests/test_api.py                # Basic
python tests/test_advanced_api.py       # Advanced features
```

## 📋 Sample Usage

```bash
# Add book
curl -X POST http://localhost:5000/api/v1/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Clean Code", "author": "Robert C. Martin", "total_copies": 5}'

# Get books with advanced features
curl "http://localhost:5000/api/v1/books?author=Robert&sort=title&page=1&limit=3"

# Borrow book
curl -X POST http://localhost:5000/api/v1/borrows \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "book_id": 1}'

# Return book
curl -X PUT http://localhost:5000/api/v1/borrows/1/return
```

## 📊 Database

**Auto-generated with sample data:**
- 4 books: Clean Code, Design Patterns, Effective Python, Flask Web Development
- 3 borrow records from 2 different users

## � Info

- **Student**: Nguyễn Bằng Anh (22021101)
- **Course**: INT3505E_02 - Week 03 API Design
- **Tech**: Flask + SQLite + RESTful API
