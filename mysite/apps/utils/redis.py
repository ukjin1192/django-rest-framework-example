#!usr/bin/python
# -*- coding:utf-8 -*-

from django.core.cache import cache
from django_redis import get_redis_connection

con = get_redis_connection('default')


def manage_cache():
    """
    Manage cache
    """
    cache.set('foo', 'bar', timeout=10)   # Create cache
    cache.get('foo')                      # Retrieve cache value
    con.expire(':1:foo', 100)             # Extend cache TTL
    cache.delete('foo')                   # Delete cache

    return None
