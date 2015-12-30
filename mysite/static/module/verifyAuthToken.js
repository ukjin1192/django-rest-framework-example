'use strict';

var $ = require('jquery');
var setCSRFToken = require('./setCSRFToken');

module.exports = function verifyAuthToken() {
  setCSRFToken();
  
  $.ajax({
    url: '/api-token-verify/',
    type: 'POST',
    data: {
      'token': localStorage.getItem('token')
    }
  }).done(function(data) {
    console.log(data);
    $('#login-info').text(localStorage.getItem('email'));
  }).fail(function(data) {
    console.log(data);
    $('#login-info').text('Not logged in');
    localStorage.clear();
  }); 
  return;
}
