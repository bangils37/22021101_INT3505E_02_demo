'use strict';

function deprecationHeaders(options = {}) {
  return function (req, res, next) {
    res.set('Deprecation', 'true');
    if (options.sunset) {
      res.set('Sunset', options.sunset);
    }
    if (options.link) {
      res.set('Link', `<${options.link}>; rel="deprecation"; type="text/html"`);
    }
    next();
  };
}

module.exports = { deprecationHeaders };