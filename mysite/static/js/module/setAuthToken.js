'use strict';

var $ = require('jquery');

module.exports = function setAuthToken() {
  $.ajaxSetup({
    headers: {
      'Authorization': 'JWT ' + localStorage.getItem('token')
    }
  });
  return;
}
