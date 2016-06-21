# -*- coding: utf-8 -*-
# __author__ = xutao


class Config(object):
    """
        just for config class
    """

    OVA_PATH = "/root/ovftool/"

    OVFTOOL_LOG = "/root/ovftool.log"

    TOEKN = "OVF_TEST"

    PAAS_HOST = ""  # IP:PORT

    OVF_TOKEN = "OVF_TEST"

    DOWNLOAD_PATH = "/var/tmp/downloads"

    CALLBACK_TOKEN = "CALLBACK_TEST"

    REDIS_URL = 'redis://localhost:6379/1'

    MAIL_SERVER = 'mail.yun-idc.com'

    MAIL_USERNAME = r"cds\cdsservice"

    ADMINS = ['cdsservice@yun-idc.com']

    MAIL_PASSWORD = 'yun-idc.com'

    DOWNLOAD_PATH = "/root/ovftool/"





class DevelopmentConfig(Config):
    """
        devlopment conofig
    """
    TOKEN = "TEST"