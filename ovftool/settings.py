# -*- coding: utf-8 -*-
# __author__ = xutao


class Config(object):
    """
        just for config class
    """

    OVA_PATH = "/data/transmission-daemon/downloads"

    OVFTOOL_LOG = "/root/ovftool.log"

    TOEKN = "OVF_TEST"

    PAAS_HOST = "114.112.92.254:8888"  # IP:PORT

    CALLBACK_TOKEN = "CALLBACK_TEST"

    REDIS_URL = 'redis://:cds-china@localhost:6379/1'

    MAIL_SERVER = 'mail.163.com'

    MAIL_USERNAME = r"cds\cdsservice"

    ADMINS = ['cc@163.com']

    MAIL_PASSWORD = 'cccc'

    DOWNLOAD_PATH = "/data/transmission-daemon/downloads"


class DevelopmentConfig(Config):
    """
        devlopment conofig
    """
    TOKEN = "OVF_TEST"
