# Demo CQRS (Command Query Responsibility Segregation)

Demo này minh họa một cách đơn giản cách hoạt động của CQRS bằng cách tách biệt các thao tác ghi (Command) và đọc (Query) cho một danh sách các sản phẩm.

### Cấu trúc thư mục

```
week11/
└── CQRS/
    ├── README.md
    ├── command.js
    ├── query.js
    └── index.js
```

### Các bước chạy demo

1.  **Mở Terminal:** Điều hướng đến thư mục `week11/CQRS` trong terminal của bạn.
    ```bash
    cd d:\AnhNB\22021101_INT3505E_02_demo\week11\CQRS
    ```
2.  **Chạy ứng dụng:** Thực thi tệp `index.js` bằng Node.js.
    ```bash
    node index.js
    ```

### Kết quả mong đợi

Bạn sẽ thấy các thông báo trong console hiển thị quá trình thêm sản phẩm (Command) và sau đó là truy vấn danh sách sản phẩm (Query), minh họa sự tách biệt giữa hai luồng này.