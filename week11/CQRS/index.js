// index.js - Chạy demo CQRS

const command = require('./command');
const query = require('./query');

console.log('--- Bắt đầu Demo CQRS ---');

// Bước 1: Thao tác ghi (Command Model)
console.log('\n--- Thao tác ghi (Command Model) ---');
command.addProduct({ id: 1, name: 'Laptop' });
command.addProduct({ id: 2, name: 'Mouse' });
command.addProduct({ id: 3, name: 'Keyboard' });

// Trong một hệ thống CQRS thực tế, Query Model sẽ cập nhật dữ liệu của nó
// thông qua việc lắng nghe các sự kiện. Ở đây, chúng ta mô phỏng việc này.
query.updateReadModel(command.getProducts());

// Bước 2: Thao tác đọc (Query Model)
console.log('\n--- Thao tác đọc (Query Model) ---');
let allProducts = query.getAllProducts();
console.log('Tất cả sản phẩm:', allProducts);

let product1 = query.getProductById(1);
console.log('Sản phẩm ID 1:', product1);

// Bước 3: Cập nhật sản phẩm (Command Model)
console.log('\n--- Cập nhật sản phẩm (Command Model) ---');
command.updateProduct(2, 'Gaming Mouse');

// Mô phỏng cập nhật Query Model sau khi Command thực hiện
query.updateReadModel(command.getProducts());

// Bước 4: Đọc lại sau khi cập nhật (Query Model)
console.log('\n--- Đọc lại sau khi cập nhật (Query Model) ---');
allProducts = query.getAllProducts();
console.log('Tất cả sản phẩm sau cập nhật:', allProducts);

// Bước 5: Xóa sản phẩm (Command Model)
console.log('\n--- Xóa sản phẩm (Command Model) ---');
command.deleteProduct(3);

// Mô phỏng cập nhật Query Model sau khi Command thực hiện
query.updateReadModel(command.getProducts());

// Bước 6: Đọc lại sau khi xóa (Query Model)
console.log('\n--- Đọc lại sau khi xóa (Query Model) ---');
allProducts = query.getAllProducts();
console.log('Tất cả sản phẩm sau xóa:', allProducts);

console.log('\n--- Kết thúc Demo CQRS ---');