# BTVN Buổi trước

## Câu hỏi

Tại sao không gộp Data Modeling và Resource Design?

## Trả lời

Không nên gộp Data Modeling và Resource Design vì hai phần có mục tiêu khác nhau.
Data Modeling tập trung vào cấu trúc và quan hệ trong database, còn Resource Design hướng đến cách cung cấp dữ liệu cho client.
Nếu gộp chung, API sẽ bị ràng buộc theo cấu trúc DB, dẫn đến phải gọi nhiều API nhỏ (n+1 query problem), tốn hiệu năng và khó đồng bộ.
Tách riêng giúp API linh hoạt hơn, có thể gom dữ liệu từ nhiều bảng và phục vụ client hiệu quả hơn.