# -*- coding: utf-8 -*-
# __author__ = xutao

import os
import socket
import logging
import logging.config
from logging.handlers import SMTPHandler
import yaml
from celery import Celery


from flask import Flask
from ovftool.settings import DevelopmentConfig

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

hostname = socket.gethostname().capitalize().replace('.', '_').replace('-', '')

# create flask app
ovftool_app = Flask(__name__)


try:
    ovftool_app.config.from_object('ovftool.settings.%sConfig' % hostname)
except Exception as e:
    ovftool_app.config.from_object(DevelopmentConfig)

ovftool_app.config.from_envvar('OVFTOOL_SETTINGS', silent=True)

config = ovftool_app.config


def configure_log(app):
    logging.config.dictConfig(yaml.load(open('%s/ovftool/log.yaml' % BASE_DIR)))

    if not app.debug:

        mail_handler = SMTPHandler(
            app.config['MAIL_SERVER'],
            app.config['MAIL_USERNAME'],
            app.config['ADMINS'],
            'Server Error!',
            (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        )

        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        app.logger.addHandler(mail_handler)

configure_log(ovftool_app)


def make_celery(app):
    """
        构造 celery
    :param app:
    :return:
    """
    broker_url = app.config["REDIS_URL"]
    backend_url = app.config["REDIS_URL"]

    celery = Celery("ovftool_celery", broker=broker_url, backend=backend_url)

    celery.conf.update(CELERYBEAT_SCHEDULE={
    }, CELERY_ENABLE_UTC=True)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(ovftool_app)

print(celery)

import ovftool.celery_task

from .api_v1 import api_bp
ovftool_app.register_blueprint(api_bp, url_prefix="/api")