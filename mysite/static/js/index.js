'use strict';

var $ = require('jquery');
var foo = require('./module/foo');

console.log(foo(1,2,3,4));

function setCSRFToken() {
  $.ajaxSetup({
    headers: {
      'X-CSRFToken': $.cookie('csrftoken')
    }
  });
}

function setAuthToken() {
  $.ajaxSetup({
    headers: {
      'Authorization': 'JWT ' + localStorage.getItem('token')
    }
  });
}

function clearAuthToken() {
  $.ajaxSetup({
    headers: {
      'Authorization': null
    }
  });
}

function obtainAuthToken(data) {
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
}

function refreshAuthToken() {
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
}

function verifyAuthToken() {
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
}

$(document).on('submit', '#signup-form', function(event) {
  event.preventDefault();
  
  var signupForm = $(this);
  var formData = new FormData();
  var loginData = new FormData();
  
  formData.append('email', signupForm.find('[name="email"]').val());
  formData.append('username', signupForm.find('[name="username"]').val());
  formData.append('password', signupForm.find('[name="password"]').val());
  
  loginData.append('email', signupForm.find('[name="email"]').val());
  loginData.append('password', signupForm.find('[name="password"]').val());
  
  setCSRFToken();
  
  $.ajax({
    url: '/api/users/',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false
  }).done(function(data) {
    obtainAuthToken(loginData);
  }).fail(function(data) {
    console.log('Login failed');
    console.log(data);
  }); 
});

$(document).on('submit', '#login-form', function(event) {
  event.preventDefault();
  
  var loginForm = $(this);
  var formData = new FormData();
  
  formData.append('email', loginForm.find('[name="email"]').val());
  formData.append('password', loginForm.find('[name="password"]').val());
  
  obtainAuthToken(formData);
});

$(document).on('click', '#logout-btn', function() {
  clearAuthToken();
  localStorage.clear();
});

$(document).on('click', '#user-profile-btn', function() {
  if (localStorage.getItem('user_id') != null) {
    var userID = localStorage.getItem('user_id');
    
    setCSRFToken();
    setAuthToken();
    
    $.ajax({
      url: '/api/users/' + userID + '/',
      type: 'GET'
    }).done(function(data) {
      console.log(data);
    }).fail(function(data) {
      console.log('Get user profile failed');
      console.log(data);
    }); 
  }
});

$(document).on('submit', '#update-user-form', function(event) {
  event.preventDefault();
  
  if (localStorage.getItem('user_id') != null) {
    var userID = localStorage.getItem('user_id');
    var updateUserForm = $(this);
    var formData = new FormData();
    
    if (updateUserForm.find('[name="email"]').val() != '' && updateUserForm.find('[name="original-password"]').val() != '') {
      formData.append('email', updateUserForm.find('[name="email"]').val());
      formData.append('original-password', updateUserForm.find('[name="original-password"]').val());
    }
    if (updateUserForm.find('[name="username"]').val() != '') 
      formData.append('username', updateUserForm.find('[name="username"]').val());
    if (updateUserForm.find('[name="original-password"]').val() != '' && updateUserForm.find('[name="password"]').val() != '') {
      formData.append('original-password', updateUserForm.find('[name="original-password"]').val());
      formData.append('password', updateUserForm.find('[name="password"]').val());
    }
    if (updateUserForm.find('[name="deactivate"]').is(':checked') == true && updateUserForm.find('[name="original-password"]').val() != '') { 
      formData.append('original-password', updateUserForm.find('[name="original-password"]').val());
      formData.append('is_active', false);
    }
    
    setCSRFToken();
    setAuthToken();
    
    $.ajax({
      url: '/api/users/' + userID + '/',
      type: 'PATCH',
      data: formData,
      contentType: false,
      processData: false
    }).done(function(data) {
      console.log(data);
      if (updateUserForm.find('[name="email"]').val() != '' && updateUserForm.find('[name="original-password"]').val() != '') {
        clearAuthToken();
        
        var loginData = new FormData();
        
        loginData.append('email', updateUserForm.find('[name="email"]').val());
        loginData.append('password', updateUserForm.find('[name="original-password"]').val());
        
        obtainAuthToken(loginData);
      }
      if (updateUserForm.find('[name="username"]').val() != '') 
        localStorage.setItem('username', updateUserForm.find('[name="username"]').val());
      if (updateUserForm.find('[name="original-password"]').val() != '' && updateUserForm.find('[name="password"]').val() != '') {
        clearAuthToken();
        
        var loginData = new FormData();
        
        loginData.append('email', localStorage.getItem('email'));
        loginData.append('password', updateUserForm.find('[name="password"]').val());
        
        obtainAuthToken(loginData);
      }
      if (updateUserForm.find('[name="deactivate"]').is(':checked') == true && updateUserForm.find('[name="original-password"]').val() != '') 
        localStorage.clear();
    }).fail(function(data) {
      console.log('Update user profile failed');
      console.log(data);
    }); 
  }
});

$(document).ready(function() {
  verifyAuthToken();
});
