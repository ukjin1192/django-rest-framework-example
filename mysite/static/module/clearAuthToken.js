'use strict';

var $ = require('jquery');

module.exports = function clearAuthToken() {
  $.ajaxSetup({
    headers: {
      'Authorization': null
    }
  });
  return;
}
