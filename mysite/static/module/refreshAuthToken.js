'use strict';

var $ = require('jquery');
var setCSRFToken = require('./setCSRFToken');

module.exports = function refreshAuthToken() {
  setCSRFToken();
  
  $.ajax({
    url: '/api-token-refresh/',
    type: 'POST',
    data: {
      'token': localStorage.getItem('token')
    }
  }).done(function(data) {
    console.log(data);
    localStorage.setItem('token', data['token']);
  }).fail(function(data) {
    console.log(data);
  }); 
  return;
}
