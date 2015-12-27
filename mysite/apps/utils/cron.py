#!usr/bin/python
# -*- coding:utf-8 -*-

from captcha.models import CaptchaStore
from celery import task
from datetime import datetime


@task()
def clear_expired_captcha(*args, **kwargs):
    """
    Clear expired captcha
    """
    CaptchaStore.objects.filter(expiration__lt=datetime.utcnow()).delete()
    return None
