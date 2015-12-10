# -*- coding: utf-8 -*-

from django.conf.urls import url
from main.views import api_root, UserViewSet, ArticleViewSet, CommentViewSet
from rest_framework.urlpatterns import format_suffix_patterns


user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
article_list = ArticleViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
article_detail = ArticleViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
comment_detail = CommentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = format_suffix_patterns([
    url(
        r'^$', 
        api_root
    ),
    url(
        r'^users/$',
        user_list,
        name='user-list'
    ),
    url(
        r'^users/(?P<pk>[0-9]+)/$',
        user_detail,
        name='user-detail'
    ),
    url(
        r'^articles/$',
        article_list,
        name='article-list'
    ),
    url(
        r'^articles/(?P<pk>[0-9]+)/$',
        article_detail,
        name='article-detail'
    ),
    url(
        r'^comments/$',
        comment_list,
        name='comment-list'
    ),
    url(
        r'^comments/(?P<pk>[0-9]+)/$',
        comment_detail,
        name='comment-detail'
    ),
])
