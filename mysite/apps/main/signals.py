#!usr/bin/python
# -*- coding: utf-8 -*-

from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import User, Comment


@receiver(post_save, sender=User)
def do_something_when_user_created(sender, instance, created, **kwargs):
    """
    Do something when user created
    """
    if created == True and instance.is_active == True:
        pass
