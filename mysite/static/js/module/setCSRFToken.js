'use strict';

var $ = require('jquery');

module.exports = function setCSRFToken() {
  $.ajaxSetup({
    headers: {
      'X-CSRFToken': $.cookie('csrftoken')
    }
  });
  return;
}
