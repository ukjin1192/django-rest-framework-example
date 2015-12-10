#!usr/bin/python
# -*- coding:utf-8 -*-

from django.conf import settings
from django.template import Library

register = Library()


@register.filter
def get_settings_variable(variable_name):
    """
    Get settings variable
    Parameter: variable name
    """
    return getattr(settings, variable_name, None)
