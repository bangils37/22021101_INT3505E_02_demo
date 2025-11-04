'use strict';

var utils = require('../utils/writer.js');
var Default = require('../service/DefaultService');

module.exports.productsGET = function productsGET (req, res, next) {
  Default.productsGET()
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.productsIdDELETE = function productsIdDELETE (req, res, next, id) {
  Default.productsIdDELETE(id)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.productsIdGET = function productsIdGET (req, res, next, id) {
  Default.productsIdGET(id)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.productsIdPUT = function productsIdPUT (req, res, next, body, id) {
  Default.productsIdPUT(body, id)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.productsPOST = function productsPOST (req, res, next, body) {
  Default.productsPOST(body)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};
