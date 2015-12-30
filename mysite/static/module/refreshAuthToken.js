'use strict';

var $ = require('jquery');

module.exports = function refreshAuthToken() {
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
