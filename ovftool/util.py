# -*- coding: utf-8 -*-
# __author__ = xutao


# just for ovftool func
import subprocess
import requests
from subprocess import PIPE
from ovftool import config
import logging
import traceback

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
        print("222222222222222222222")
	if tpl_folder:
	    print("11111111")
            process = subprocess.Popen("ovftool --machineOutput"
                                       " --acceptAllEulas  -dm=thin --noSSLVerify -vf='%s' -ds='%s'"
                                       " %s 'vi://%s:%s@%s/%s/host/%s'" % (tpl_folder, datastore, ova_path, username, password, host, datacenter, cluster_name), shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        else:
	    print("yyyyyyy")
	    process_str = "ovftool --machineOutput -dm=thin --acceptAllEulas  --noSSLVerify  -ds='%s' %s 'vi://%s:%s@%s/%s/host/%s'" % (datastore, ova_path, username, password, host, datacenter, cluster_name) 
	    print(process_str) 
            process = subprocess.Popen(process_str, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        print("yyyyyyyyyyyyyyyy")
	result = process.communicate()
	print(result)
	if result:
	    print("deploy result isi vvvvvvvv")
        else:
	    print("deploy result is exists")
	delete_process = subprocess.Popen("rm -fv %s" % ova_path, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        delete_result = delete_process.communicate()
	#print("delete tpl result is %s" % delete_result)
        logger.debug("delete ova file:%s" % ova_path)
        for res in result:
            if "SUCCESS" in res:
                logger.debug("ova:%s convert success then to chmod" % vm_name)
                return True, "deploy ova success"
            elif "ERROR" in res:
		print("just for deploy is error ova_path is %s" % ova_path)
                return False, res
    except Exception as e:
        logger.error("deploy ovftool when catch error:%s" % str(e))
        logger.error("ssss is %s" % traceback.format_exc())
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
        process = subprocess.Popen("ovftool -o --machineOutput"
                                   "  --noSSLVerify "
                                   " 'vi://%s:%s@%s/%s/vm/%s'"
                                   " '%s'" % (username, password, host, datacenter, vm_name, ova_path), shell=True
                                   ,stdin=PIPE, stdout=PIPE, stderr=PIPE)
        result = process.communicate()
        logger.debug("convert vm:%s to ova result is %s" % (vm_name, result))
        for res in result:
            if "SUCCESS" in res:
                chmod_process = subprocess.Popen("chmod 644 %s" % ova_path, shell=True)
                chmod_process.communicate()
                logger.debug("ova:%s convert success and chmod success" % vm_name)
                return True, "success"
            elif "ERROR" in res:
                return False, result

    except Exception as e:
        logger.error("convert ova when catch error:%s" % str(e))
        return False, str(e)


def task_callback(task_id, status, result):
    """
        任务无论成功还是失败都开始回调
    :param task_id:
    :return:
    """

    url = "http://%s/stat/task/callback/" % config["PAAS_HOST"]

    data = {
        "task_id": task_id,
        "status": status,
        "result": result,
        "token": config["CALLBACK_TOKEN"]
    }

    respone = requests.post(url, data=data)

    if respone.ok:
        logger.debug("task:%s update ok" % task_id)
    logger.info("server is not work just for 500 task:%s" % task_id)
    return False



