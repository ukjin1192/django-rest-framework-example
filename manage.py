#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os
import sys

ROOT_DIR = os.path.dirname(__file__)

# Get sensitive configuration
config = ConfigParser.ConfigParser()
config.read(ROOT_DIR + '/conf/sensitive/configuration.ini')

PROJECT_NAME = config.get('django', 'project_name')

if __name__ == '__main__':
    # Development mode
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', PROJECT_NAME + '.settings.dev')

    # Production mode
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', PROJECT_NAME + '.settings.prod')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
