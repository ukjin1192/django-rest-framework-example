# -*- coding: utf-8 -*-

from django.conf import settings
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

if settings.DEBUG == True:
    urlpatterns += [
        # Inspection tool
        url(
            r'^silk/', 
            include('silk.urls', namespace='silk')
        ),
    ]
