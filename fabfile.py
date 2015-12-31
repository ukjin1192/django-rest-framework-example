#!/bin/bash
import os
from ConfigParser import ConfigParser
from fabric.api import *

ROOT_DIR = os.path.dirname(__file__)

# Get sensitive configuration
config = ConfigParser()
config.read(ROOT_DIR + '/conf/sensitive/configuration.ini')

PROJECT_NAME = config.get('django', 'project_name')

# Remote Deploy Server Information
env.hosts = config.get('fabric', 'ip_address')
env.user = config.get('fabric', 'username')
env.key_filename = ROOT_DIR + "/conf/sensitive/remote_server.pem"
env.port = 22


def docker_onboot():
    local("sudo service nginx start")
    local("sudo service mysql start")
    local("sudo service redis-server start")
    local("sudo service rabbitmq-server start")


def run_uwsgi():
    local("sudo uwsgi --uid www-data --gid www-data --emperor /etc/uwsgi/vassals --master --die-on-term --daemonize=" + ROOT_DIR + "/logs/uwsgi.log")


def stop_uwsgi():
    with settings(warn_only=True):
        local("ps -ef | grep uwsgi | grep -v grep | awk '{print $2}' | xargs kill -15")


def run_shell():
    with lcd(ROOT_DIR):
        try:
            local("./manage.py shell_plus")
        except:
            local("./manage.py shell")


def run_dbshell():
    with lcd(ROOT_DIR):
        local("./manage.py dbshell")


def run_server():
    with lcd(ROOT_DIR):
        local("./manage.py runserver 0.0.0.0:8000")


def run_test():
    with lcd(ROOT_DIR):
        local("./manage.py test main")


def run_celery():
    with lcd(ROOT_DIR):
        local("./manage.py celeryd_detach --logfile=logs/celery_daemon.log --pidfile=logs/celery_daemon.pid")
        local("./manage.py celery beat --logfile=logs/celery_beat.log --pidfile=logs/celery_beat.pid --detach")


def stop_celery():
    with settings(warn_only=True):
        local("ps auxww | grep 'celery worker' | grep -v grep | awk '{print $2}' | xargs kill -15")
    with settings(warn_only=True):
        local("ps auxww | grep 'celery beat' | grep -v grep | awk '{print $2}' | xargs kill -15")


def clear_celery_tasks():
    with lcd(ROOT_DIR):
        local("./manage.py celery purge")


def clear_silk_logs():
    with lcd(ROOT_DIR):
        local("./manage.py silk_clear_request_log")


def update_staticfiles():
    with lcd(ROOT_DIR + "/" + PROJECT_NAME + "/static/"):
        if int(config.get('django', 'development_mode')) == 1:
            # Development mode
            local("webpack")
        else:
            # Production mode
            local("production_mode=1 webpack")
    with lcd(ROOT_DIR):
        local("./manage.py collectstatic --noinput")


def remote_deploy():
    with cd(ROOT_DIR):
        sudo("git pull origin master")
        with settings(warn_only=True):
            sudo("ps auxww | grep 'celery worker' | grep -v grep | awk '{print $2}' | xargs kill -15")
        with settings(warn_only=True):
            sudo("ps auxww | grep 'celery beat' | grep -v grep | awk '{print $2}' | xargs kill -15")
        with settings(warn_only=True):
            sudo("ps -ef | grep uwsgi | grep -v grep | awk '{print $2}' | xargs kill -15")
        sudo("./manage.py celeryd_detach --logfile=logs/celery_daemon.log --pidfile=logs/celery_daemon.pid")
        sudo("./manage.py celery beat --logfile=logs/celery_beat.log --pidfile=logs/celery_beat.pid --detach")
        sudo("uwsgi --uid www-data --gid www-data --emperor /etc/uwsgi/vassals --master --die-on-term --daemonize=" + ROOT_DIR + "/logs/uwsgi.log")
