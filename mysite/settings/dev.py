#!usr/bin/python
# -*- coding:utf-8 -*-

from base import *

# Debugging option
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = [
    '*',
]
INTERNAL_IPS = (
    '127.0.0.1',
)

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config.get('django', 'project_name'),
        'USER': 'root',
        'PASSWORD': config.get('mysql:development', 'password'),
        'HOST': '',
        'PORT': '',
        'DEFAULT-CHARACTER-SET': 'utf8',
    }
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Silk is live profiling and inspection tool
RUN_SILK = DEBUG

if RUN_SILK:
    # Silk should be the first placement
    MIDDLEWARE_CLASSES = ('silk.middleware.SilkyMiddleware', ) + MIDDLEWARE_CLASSES

    INSTALLED_APPS += (
        'silk',
    )

    # Silk settings
    SILKY_AUTHENTICATION = True
    SILKY_PERMISSIONS = lambda user: user.is_staff
    SILKY_MAX_REQUEST_BODY_SIZE = -1        # Silk takes anything <0 as no limit
    SILKY_MAX_RESPONSE_BODY_SIZE = 1024     # If response body>1024kb, ignore
