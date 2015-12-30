'use strict';

// Load bootstrap with custom configuration
require('bootstrap-webpack!./bootstrap.config.js');
require('./styles.scss');

var setAuthToken = require('./module/setAuthToken');
var clearAuthToken = require('./module/clearAuthToken');
var obtainAuthToken = require('./module/obtainAuthToken');
var refreshAuthToken = require('./module/refreshAuthToken');
var verifyAuthToken = require('./module/verifyAuthToken');

$(document).on('click', '#launch-modal-btn', function() {
  $('#modal-test').modal('show');
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

$(document).on('click', '#refresh-captcha-btn', function() {
  $.ajax({
    url: '/captcha/refresh/',
    type: 'GET'
  }).done(function(data) {
    console.log('Succeed to refresh captcha');
    console.log(data);

    $('#captcha-image').attr('src', data.image_url);
    $('#create-user-form').find('[name="captcha-key"]').val(data.key);
  }).fail(function(data) {
    console.log('Failed to refresh captcha');
    console.log(data);
  }); 
});

$(document).on('submit', '#create-user-form', function(event) {
  event.preventDefault();

  var signupForm = $(this);
  var formData = new FormData();
  var loginData = new FormData();

  formData.append('email', signupForm.find('[name="email"]').val());
  formData.append('username', signupForm.find('[name="username"]').val());
  formData.append('password', signupForm.find('[name="password"]').val());
  formData.append('captcha-key', signupForm.find('[name="captcha-key"]').val());
  formData.append('captcha-value', signupForm.find('[name="captcha-value"]').val());

  loginData.append('email', signupForm.find('[name="email"]').val());
  loginData.append('password', signupForm.find('[name="password"]').val());

  $.ajax({
    url: '/api/users/',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false
  }).done(function(data) {
    if (data.state == false) {
      console.log('Failed to create user');
      console.log(data);
    } else {
      console.log('Succeed to create user');
      console.log(data);
      obtainAuthToken(loginData);
    }
  }).fail(function(data) {
    console.log('Failed to create user');
    console.log(data);
  }); 
});

$(document).on('click', '#read-user-btn', function() {
  if (localStorage.getItem('user_id') != null) {
    var userID = localStorage.getItem('user_id');

    setAuthToken();

    $.ajax({
      url: '/api/users/' + userID + '/',
      type: 'GET'
    }).done(function(data) {
      console.log('Succeed to read user');
      console.log(data);
    }).fail(function(data) {
      console.log('Failed to read user');
      console.log(data);
    }); 
  }
});

$(document).on('submit', '#update-user-email-form', function(event) {
  event.preventDefault();

  if (localStorage.getItem('user_id') != null) {
    var userID = localStorage.getItem('user_id');
    var updateUserEmailForm = $(this);
    var formData = new FormData();

    formData.append('email', updateUserEmailForm.find('[name="email"]').val());
    formData.append('original-password', updateUserEmailForm.find('[name="original-password"]').val());

    setAuthToken();

    $.ajax({
      url: '/api/users/' + userID + '/',
      type: 'PATCH',
      data: formData,
      contentType: false,
      processData: false
    }).done(function(data) {
      if (data.state == false) {
        console.log('Failed to update user email');
        console.log(data);
      } else {
        console.log('Succeed to update user email');
        console.log(data);

        clearAuthToken();

        var loginData = new FormData();

        loginData.append('email', updateUserEmailForm.find('[name="email"]').val());
        loginData.append('password', updateUserEmailForm.find('[name="original-password"]').val());

        obtainAuthToken(loginData);
      }
    }).fail(function(data) {
      console.log('Failed to update user email');
      console.log(data);
    }); 
  }
});

$(document).on('submit', '#update-user-username-form', function(event) {
  event.preventDefault();

  if (localStorage.getItem('user_id') != null) {
    var userID = localStorage.getItem('user_id');
    var updateUserUsernameForm = $(this);
    var formData = new FormData();

    formData.append('username', updateUserUsernameForm.find('[name="username"]').val());

    setAuthToken();

    $.ajax({
      url: '/api/users/' + userID + '/',
      type: 'PATCH',
      data: formData,
      contentType: false,
      processData: false
    }).done(function(data) {
      console.log('Succeed to update user username');
      console.log(data);
      localStorage.setItem('username', updateUserUsernameForm.find('[name="username"]').val());
    }).fail(function(data) {
      console.log('Failed to update user username');
      console.log(data);
    }); 
  }
});

$(document).on('submit', '#update-user-password-form', function(event) {
  event.preventDefault();

  if (localStorage.getItem('user_id') != null) {
    var userID = localStorage.getItem('user_id');
    var updateUserPasswordForm = $(this);
    var formData = new FormData();

    formData.append('original-password', updateUserPasswordForm.find('[name="original-password"]').val());
    formData.append('password', updateUserPasswordForm.find('[name="password"]').val());

    setAuthToken();

    $.ajax({
      url: '/api/users/' + userID + '/',
      type: 'PATCH',
      data: formData,
      contentType: false,
      processData: false
    }).done(function(data) {
      if (data.state == false) {
        console.log('Failed to update user password');
        console.log(data);
      } else {
        console.log('Succeed to update user password');
        console.log(data);

        clearAuthToken();

        var loginData = new FormData();

        loginData.append('email', localStorage.getItem('email'));
        loginData.append('password', updateUserPasswordForm.find('[name="password"]').val());

        obtainAuthToken(loginData);
      }
    }).fail(function(data) {
      console.log('Failed to update user password');
      console.log(data);
    }); 
  }
});

$(document).on('submit', '#delete-user-form', function(event) {
  event.preventDefault();

  if (localStorage.getItem('user_id') != null) {
    var userID = localStorage.getItem('user_id');
    var deleteUserForm = $(this);
    var formData = new FormData();

    formData.append('original-password', deleteUserForm.find('[name="original-password"]').val());
    formData.append('is_active', false);

    setAuthToken();

    $.ajax({
      url: '/api/users/' + userID + '/',
      type: 'PATCH',
      data: formData,
      contentType: false,
      processData: false
    }).done(function(data) {
      if (data.state == false) {
        console.log('Failed to delete user');
        console.log(data);
      } else {
        console.log('Succeed to delete user');
        console.log(data);
        localStorage.clear();
      }
    }).fail(function(data) {
      console.log('Failed to delete user');
      console.log(data);
    }); 
  }
});

$(document).on('submit', '#create-article-form', function(event) {
  event.preventDefault();

  var createArticleForm = $(this);
  var formData = new FormData();

  formData.append('title', createArticleForm.find('[name="title"]').val());
  formData.append('context', createArticleForm.find('[name="context"]').val());

  setAuthToken();

  $.ajax({
    url: '/api/articles/',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false
  }).done(function(data) {
    console.log('Succeed to create article');
    console.log(data);
  }).fail(function(data) {
    console.log('Failed to create article');
    console.log(data);
  }); 
}); 

$(document).on('submit', '#read-article-form', function(event) {
  event.preventDefault();

  var articleID = $(this).find('[name="article-id"]').val().toString();

  $.ajax({
    url: '/api/articles/' + articleID + '/',
    type: 'GET'
  }).done(function(data) {
    console.log('Succeed to read article');
    console.log(data);
  }).fail(function(data) {
    console.log('Failed to read article');
    console.log(data);
  }); 
}); 

$(document).on('submit', '#update-article-form', function(event) {
  event.preventDefault();

  var updateArticleForm = $(this);
  var formData = new FormData();
  var articleID = updateArticleForm.find('[name="article-id"]').val().toString();

  formData.append('title', updateArticleForm.find('[name="title"]').val());
  formData.append('context', updateArticleForm.find('[name="context"]').val());

  setAuthToken();

  $.ajax({
    url: '/api/articles/' + articleID + '/',
    type: 'PATCH',
    data: formData,
    contentType: false,
    processData: false
  }).done(function(data) {
    console.log('Succeed to update article');
    console.log(data);
  }).fail(function(data) {
    console.log('Failed to update article');
    console.log(data);
  }); 
});

$(document).on('submit', '#delete-article-form', function(event) {
  event.preventDefault();

  var articleID = $(this).find('[name="article-id"]').val().toString();
  var formData = new FormData();

  formData.append('state', 'deleted');

  setAuthToken();

  $.ajax({
    url: '/api/articles/' + articleID + '/',
    type: 'PATCH',
    data: formData,
    contentType: false,
    processData: false
  }).done(function(data) {
    console.log('Succeed to delete article');
    console.log(data);
  }).fail(function(data) {
    console.log('Failed to delete article');
    console.log(data);
  }); 
});

$(document).on('submit', '#create-comment-form', function(event) {
  event.preventDefault();

  var createCommentForm = $(this);
  var formData = new FormData();

  formData.append('article_id', createCommentForm.find('[name="article-id"]').val());
  formData.append('context', createCommentForm.find('[name="context"]').val());

  setAuthToken();

  $.ajax({
    url: '/api/comments/',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false
  }).done(function(data) {
    console.log('Succeed to create comment');
    console.log(data);
  }).fail(function(data) {
    console.log('Failed to create comment');
    console.log(data);
  }); 
}); 

$(document).on('submit', '#read-comment-form', function(event) {
  event.preventDefault();

  var commentID = $(this).find('[name="comment-id"]').val().toString();

  $.ajax({
    url: '/api/comments/' + commentID + '/',
    type: 'GET'
  }).done(function(data) {
    console.log('Succeed to read comment');
    console.log(data);
  }).fail(function(data) {
    console.log('Failed to read comment');
    console.log(data);
  }); 
}); 

$(document).on('submit', '#update-comment-form', function(event) {
  event.preventDefault();

  var updateCommentForm = $(this);
  var formData = new FormData();
  var commentID = updateCommentForm.find('[name="comment-id"]').val().toString();

  formData.append('context', updateCommentForm.find('[name="context"]').val());

  setAuthToken();

  $.ajax({
    url: '/api/comments/' + commentID + '/',
    type: 'PATCH',
    data: formData,
    contentType: false,
    processData: false
  }).done(function(data) {
    console.log('Succeed to update comment');
    console.log(data);
  }).fail(function(data) {
    console.log('Failed to update comment');
    console.log(data);
  }); 
});

$(document).on('submit', '#delete-comment-form', function(event) {
  event.preventDefault();

  var commentID = $(this).find('[name="comment-id"]').val().toString();
  var formData = new FormData();

  formData.append('state', 'deleted');

  setAuthToken();

  $.ajax({
    url: '/api/comments/' + commentID + '/',
    type: 'PATCH',
    data: formData,
    contentType: false,
    processData: false
  }).done(function(data) {
    console.log('Succeed to delete comment');
    console.log(data);
  }).fail(function(data) {
    console.log('Failed to delete comment');
    console.log(data);
  }); 
});

$(document).ready(function() {
  verifyAuthToken();
});
