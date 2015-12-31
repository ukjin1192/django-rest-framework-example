#!usr/bin/python
# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser
from django.core.wsgi import get_wsgi_application
import djcelery
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(PROJECT_DIR)
APPS_DIR = os.path.join(PROJECT_DIR, 'apps')

sys.path.insert(0, PROJECT_DIR)
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, APPS_DIR)

# Get sensitive configuration
config = ConfigParser()
config.read(ROOT_DIR + '/conf/sensitive/configuration.ini')

if int(config.get('django', 'development_mode')) == 1:
    # Development mode
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')
else:
    # Production mode
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.prod')

reload(sys)
sys.setdefaultencoding('utf-8')

application = get_wsgi_application()

# Load celery
djcelery.setup_loader()
