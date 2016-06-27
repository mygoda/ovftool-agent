# -*- coding: utf-8 -*-
# __author__ = xutao
from flask import jsonify, request
from ovftool.celery_task import convert_to_ova, deploy_ova, add_together

from ovftool.api_v1 import api_bp
from ovftool import config
import logging


@api_bp.route("/status/", methods=["GET"])
def status():
    """
        测试接口
    :return:
    """
    return jsonify({"status": "ok", "msg": "just ok"})


@api_bp.route("/ovas/", methods=["POST"])
def ovas():
    """
        转化 ova
    :return:
    """
    result = {"status": "ok", "msg": "do it"}
    if request.method == "POST":
        data = request.form
        token = data.get("token", "")
        logging.debug("this data is %s" % data)
        logging.debug("token is %s" % token)
        logging.debug("config token is %s" % config.get("TOKEN"))
        if token == config.get("TOKEN"):
            # just confirm can i do it
            logging.debug("this action can do it")
            convert_to_ova.apply_async(args=[data.get("host"), data.get("username"), data.get("password"),
                                             data.get("datacenter"), data.get("vm_name"), data.get("task_id")])
            return jsonify(result)
        else:
            logging.debug("can not do this")
            result["status"] = "forbid"
            result["msg"] = "can not do it"
            return jsonify(result)


@api_bp.route("/vms/", methods=["POST"])
def vms():
    """
        部署模板
    :return:
    """
    result = {"status": "ok", "msg": "do it"}
    if request.method == "POST":
        data = request.form
        token = data.get("token", "")
        if token == config.get("TOKEN"):
            # just confirm can i do it
            deploy_ova.apply_async(args=[data.get("username"), data.get("password"), data.get("host"),
                                             data.get("vm_name"), data.get("cluster_name"),
                                         data.get("datastore"), data.get("datacenter"), data.get("tpl_folder"), data.get("task_id ")])
            return jsonify(result)
        else:
            result["status"] = "forbid"
            result["msg"] = "can not do it"
            return jsonify(result)


@api_bp.route("/test/", methods=["GET"])
def test():
    """
        测试
    :return:
    """
    add_together.apply_async(args=[10, 20])
    return jsonify({"status": "ok", "msg": "okok"})