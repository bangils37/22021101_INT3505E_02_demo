// query.js - Xử lý các thao tác đọc (Query Model)

let readModelProducts = []; // Đây là nơi lưu trữ dữ liệu "đọc", có thể là một DB khác

function updateReadModel(productsFromCommand) {
    // Trong thực tế, Query Model sẽ lắng nghe các sự kiện từ Command Model
    // và cập nhật dữ liệu của nó một cách không đồng bộ.
    // Ở đây, chúng ta mô phỏng bằng cách sao chép dữ liệu từ Command Model.
    readModelProducts = [...productsFromCommand];
    console.log('[Query] Read Model đã được cập nhật.');
}

function getAllProducts() {
    console.log('[Query] Truy vấn tất cả sản phẩm.');
    return readModelProducts;
}

function getProductById(id) {
    console.log(`[Query] Truy vấn sản phẩm với ID: ${id}`);
    return readModelProducts.find(p => p.id === id);
}

module.exports = {
    updateReadModel,
    getAllProducts,
    getProductById
};