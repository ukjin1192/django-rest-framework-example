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

# Live profiling and inspection tool
MIDDLEWARE_CLASSES += (
    'silk.middleware.SilkyMiddleware',
)

INSTALLED_APPS += (
    'silk',
)
