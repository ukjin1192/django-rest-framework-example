#!usr/bin/python
# -*- coding:utf-8 -*-

from base import *

# Debugging option
DEBUG = False
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = [
    config.get('django', 'project_name') + '.com',
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
        'PASSWORD': config.get('mysql:production', 'password'),
        'HOST': config.get('mysql:production', 'end_point'),
        'PORT': '3306',
        'DEFAULT-CHARACTER-SET': 'utf8',
    }
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config.get('redis:production', 'end_point'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
