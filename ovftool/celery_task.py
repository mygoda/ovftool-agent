# -*- coding: utf-8 -*-
# __author__ = xutao
import traceback
from . import ovftool_app, celery
import logging
from ovftool.util import convert, deploy, task_callback
import time


@celery.task
def add_together(a, b):
    logging.debug('start add together')
    time.sleep(10)
    logging.debug("end add")
    return a + b


@celery.task
def convert_to_ova(host, username, password, datacenter, vm_name, task_id):
    """
        celery 创建 ova 模板任务
    :param host:
    :param username:
    :param password:
    :param datacenter:
    :param vm_name:
    :return:
    """
    logging.debug("start convert vm to ova")
    try:
        success, result = convert(host=host, username=username, password=password, datacenter=datacenter, vm_name=vm_name, task_id=task_id)
        if success:
            # 回调
            status = "ovf_success"
        else:
            status = "ovf_fault"

        task_callback(task_id=task_id, status=status, result=result)

    except Exception as e:
        logging.error("convert to ova catch exception:%s" % traceback.format_exc())


@celery.task
def deploy_ova(username, password, host, vm_name, cluster_name, datastore, datacenter, tpl_folder, task_id):
    """
        部署 ova 模板
    :param username:
    :param password:
    :param host:
    :param vm_name:
    :param ova_path:
    :param cluster_name:
    :param datastore:
    :param datacenter:
    :return:
    """
    logging.debug("start deploy ova")
    try:
        success, result = deploy(username=username, host=host, password=password, vm_name=vm_name,
                                 cluster_name=cluster_name, datastore=datastore, datacenter=datacenter, tpl_folder=tpl_folder, task_id=task_id)

        if success:
            # 回调
            status = "deploy_success"
        else:
            status = "deploy_fault"
        print(status)
        task_callback(task_id=task_id, status=status, result=result)

    except Exception as e:
        logging.error("deploy ova catch exception:%s" % traceback.format_exc())
