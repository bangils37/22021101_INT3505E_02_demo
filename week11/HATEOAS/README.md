# Demo HATEOAS (Hypermedia As The Engine Of Application State)

Demo này minh họa cách một API RESTful có thể triển khai HATEOAS bằng cách nhúng các liên kết siêu phương tiện vào phản hồi của nó. Client có thể điều hướng API chỉ bằng cách theo dõi các liên kết này.

### Cấu trúc thư mục

```
week11/
└── HATEOAS/
    ├── README.md
    ├── server.js
    └── package.json
```

### Các bước chạy demo

1.  **Mở Terminal:** Điều hướng đến thư mục `week11/HATEOAS` trong terminal của bạn.
    ```bash
    cd d:\AnhNB\22021101_INT3505E_02_demo\week11\HATEOAS
    ```
2.  **Cài đặt dependencies:** Cài đặt các gói cần thiết (Express và Express-HATEOAS).
    ```bash
    npm init -y
    npm install express express-hateoas-links
    ```
3.  **Chạy server:** Khởi động server Node.js.
    ```bash
    node server.js
    ```
4.  **Truy cập API:** Mở trình duyệt hoặc sử dụng công cụ như Postman để truy cập các URL sau:
    *   `http://localhost:3000/articles`
    *   `http://localhost:3000/articles/1`

### Kết quả mong đợi

Bạn sẽ thấy các phản hồi JSON chứa các liên kết (`_links`) cho phép bạn khám phá API. Ví dụ, từ danh sách bài viết, bạn có thể nhấp vào liên kết `self` của một bài viết để xem chi tiết bài viết đó, hoặc liên kết `comments` để xem bình luận của bài viết.