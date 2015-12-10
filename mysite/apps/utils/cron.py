#!usr/bin/python
# -*- coding:utf-8 -*-

from celery import task


@task()
def sample_async_task(*args, **kwargs):
    """
    Sample async task
    """
    return None
