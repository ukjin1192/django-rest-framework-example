'use strict';

var $ = require('jquery');

module.exports = function verifyAuthToken() {
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
