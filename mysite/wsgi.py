#!usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(PROJECT_DIR)
APPS_DIR = os.path.join(PROJECT_DIR, 'apps')

sys.path.insert(0, PROJECT_DIR)
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, APPS_DIR)

# For development mode
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')

# For production mode
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.prod')

reload(sys)
sys.setdefaultencoding('utf-8')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

import djcelery

djcelery.setup_loader()
