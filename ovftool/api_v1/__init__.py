# -*- coding: utf-8 -*-
# __author__ = xutao

from flask import Blueprint, current_app

api_bp = Blueprint('wechat', __name__)

from . import api