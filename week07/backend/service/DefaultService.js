'use strict';

let products = [];
let currentId = 1;

/**
 * Get all products
 *
 * returns List
 **/
exports.productsGET = function() {
  return new Promise(function(resolve, reject) {
    resolve(products);
  });
}


/**
 * Delete product by ID
 *
 * id String 
 * no response value expected for this operation
 **/
exports.productsIdDELETE = function(id) {
  return new Promise(function(resolve, reject) {
    products = products.filter(product => product.id !== id);
    resolve();
  });
}


/**
 * Get product by ID
 *
 * id String 
 * returns Product
 **/
exports.productsIdGET = function(id) {
  return new Promise(function(resolve, reject) {
    const product = products.find(product => product.id === id);
    if (product) {
      resolve(product);
    } else {
      reject({ status: 404, message: 'Product not found' });
    }
  });
}


/**
 * Update product by ID
 *
 * body ProductInput 
 * id String 
 * returns Product
 **/
exports.productsIdPUT = function(body,id) {
  return new Promise(function(resolve, reject) {
    let updatedProduct = null;
    products = products.map(product => {
      if (product.id === id) {
        updatedProduct = { ...body, id: id };
        return updatedProduct;
      }
      return product;
    });
    if (updatedProduct) {
      resolve(updatedProduct);
    } else {
      reject({ status: 404, message: 'Product not found' });
    }
  });
}


/**
 * Create a new product
 *
 * body ProductInput 
 * returns Product
 **/
exports.productsPOST = function(body) {
  return new Promise(function(resolve, reject) {
    const newProduct = { id: (currentId++).toString(), ...body };
    products.push(newProduct);
    resolve(newProduct);
  });
}

