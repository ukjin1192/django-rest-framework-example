# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token


admin.autodiscover()

urlpatterns = [
    # Admin
    url(
        r'^admin/', 
        include(admin.site.urls)
    ),
    # JSON Web Token authentication
    url(
        r'^api-token-auth/', 
        obtain_jwt_token,
    ),
    url(
        r'^api-token-refresh/', 
        refresh_jwt_token
    ),
    url(
        r'^api-token-verify/', 
        verify_jwt_token
    ),
    # Main application
    url(
        r'^api/', 
        include('main.urls')
    ),
    url(
        r'^captcha/', 
        include('captcha.urls')
    ),
    # Sample front-end page
    url(
        r'^$', 
        TemplateView.as_view(template_name='index.html')
    ),
]


if settings.RUN_SILK:
    urlpatterns += [
        # Inspection tool
        url(
            r'^silk/', 
            include('silk.urls', namespace='silk')
        ),
    ]
