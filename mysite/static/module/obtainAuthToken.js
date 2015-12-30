'use strict';

var $ = require('jquery');
var setCSRFToken = require('./setCSRFToken');

module.exports = function obtainAuthToken(data) {
  setCSRFToken();
  
  $.ajax({
    url: '/api-token-auth/',
    type: 'POST',
    data: data,
    contentType: false,
    processData: false
  }).done(function(data) {
    console.log(data);
    localStorage.setItem('token', data['token']);
    localStorage.setItem('user_id', data['user_id']);
    localStorage.setItem('email', data['email']);
    localStorage.setItem('username', data['username']);
  }).fail(function(data) {
    console.log(data);
  }); 
  return;
}
