# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = [
    # Admin
    url(
        r'^admin/', 
        include(admin.site.urls)
    ),
    # REST framework login and logout
    url(
        r'^api-auth/', 
        include('rest_framework.urls', 'rest_framework')
    ),
    # Main application
    url(
        r'^api/', 
        include('main.urls')
    ),
    # Sample front-end page
    url(
        r'^$', 
        TemplateView.as_view(template_name='index.html')
    ),
]
