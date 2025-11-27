// command.js - Xử lý các thao tác ghi (Command Model)

const products = []; // Đây là nơi lưu trữ dữ liệu "ghi"

function addProduct(product) {
    console.log(`[Command] Thêm sản phẩm: ${product.name}`);
    products.push(product);
    // Trong một hệ thống thực tế, ở đây sẽ phát ra một sự kiện (event)
    // để Query Model có thể cập nhật dữ liệu của nó.
}

function updateProduct(id, newName) {
    console.log(`[Command] Cập nhật sản phẩm ID ${id} với tên mới: ${newName}`);
    const product = products.find(p => p.id === id);
    if (product) {
        product.name = newName;
        // Phát ra sự kiện cập nhật
    } else {
        console.log(`[Command] Không tìm thấy sản phẩm với ID: ${id}`);
    }
}

function deleteProduct(id) {
    console.log(`[Command] Xóa sản phẩm ID: ${id}`);
    const index = products.findIndex(p => p.id === id);
    if (index !== -1) {
        products.splice(index, 1);
        // Phát ra sự kiện xóa
    } else {
        console.log(`[Command] Không tìm thấy sản phẩm với ID: ${id}`);
    }
}

module.exports = {
    addProduct,
    updateProduct,
    deleteProduct,
    getProducts: () => products // Chỉ để demo, trong thực tế Query Model sẽ đọc từ nguồn khác
};