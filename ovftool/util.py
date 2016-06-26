# -*- coding: utf-8 -*-
# __author__ = xutao


# just for ovftool func
import subprocess
import requests
from subprocess import PIPE
from ovftool import config
import logging


logger = logging.getLogger(__name__)


def deploy(host, username, password, vm_name, cluster_name, datastore, datacenter, tpl_folder, task_id):
    """
        部署虚拟机

    :param host:
    :param username:
    :param password:
    :param datacenter:
    :param vm_name:
    :return:
    """
    try:
        logger.info("start deploy ....")
        ova_path = "%s/%s.ova" % (config.get("DOWNLOAD_PATH"), vm_name)
        if tpl_folder:
            process = subprocess.Popen("ovftool --machineOutput --X:logLevel=verbose --X:logFile='%s'"
                                       " --acceptAllEulas  --noSSLVerify -vf='%s' -ds='%s'"
                                       " %s 'vi://%s:%s@%s/%s/host/%s'" % (config.OVFTOOL_LOG, tpl_folder, datastore, ova_path, username, password, host, datacenter, cluster_name), shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        else:
            process = subprocess.Popen("ovftool --machineOutput --X:logLevel=verbose --X:logFile='%s'"
                                       " --acceptAllEulas  --noSSLVerify  -ds='%s'"
                                       " %s 'vi://%s:%s@%s/%s/host/%s'" % (config.get("OVFTOOL_LOG"), datastore,
                                                                           ova_path, username, password, host, datacenter, cluster_name),
                                       shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        result = process.communicate()
        for res in result:
            if "SUCCESS" in res:
                logger.debug("ova:%s convert success then to chmod" % vm_name)
                return True, result
            elif "ERROR" in res:
                return False, res
    except Exception as e:
        logger.error("deploy ovftool when catch error:%s" % str(e))
        return False, str(e)


def convert(host, username, password, datacenter, vm_name, task_id):
    """
        指定虚拟机名称转化为模板
    :param host:
    :param username:
    :param password:
    :param datacenter:
    :param vm_name:
    :return:
    """
    try:
        ova_path = "%s/%s.ova" % (config.get("OVA_PATH"), vm_name)
        logger.info("start convert....")
        process = subprocess.Popen("ovftool -o --machineOutput --X:logLevel=verbose --X:logFile='%s'"
                                   "  --noSSLVerify "
                                   " 'vi://%s:%s@%s/%s/vm/%s'"
                                   " '%s'" % (config.get("OVFTOOL_LOG"), username, password, host, datacenter, vm_name, ova_path), shell=True
                                   ,stdin=PIPE, stdout=PIPE, stderr=PIPE)
        result = process.communicate()
        for res in result:
            if "SUCCESS" in res:
                chmod_process = subprocess.Popen("chmod 644 %s" % ova_path, shell=True)
                chmod_process.communicate()
                logger.debug("ova:%s convert success and chmod success" % vm_name)
                return True, "success"
            elif "ERROR" in res:
                return False, res

    except Exception as e:
        logger.error("convert ova when catch error:%s" % str(e))
        return False, str(e)


def task_callback(task_id, status, result):
    """
        任务无论成功还是失败都开始回调
    :param task_id:
    :return:
    """

    url = "http://%s/stat/task/callback/" % config.PAAS_HOST

    data = {
        "task_id": task_id,
        "status": status,
        "result": result,
        "token": config.CALLBACK_TOKEN
    }

    respone = requests.post(url, data=data)

    if respone.ok:
        logger.debug("task:%s update ok" % task_id)
    logger.info("server is not work just for 500 task:%s" % task_id)
    return False



