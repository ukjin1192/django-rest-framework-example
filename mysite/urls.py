# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from main import views
from rest_framework.routers import DefaultRouter


admin.autodiscover()

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'articles', views.ArticleViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = patterns('',

    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # REST framework login and logout
    url(r'^api-auth/', include('rest_framework.urls', 'rest_framework')),

    # Router
    url(r'^', include(router.urls)),
)
