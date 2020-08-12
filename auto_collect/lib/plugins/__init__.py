# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: Yfh
"""
from importlib import import_module
from common.constant.constant_plugin import PLUGIN_DICT


def get_server_info(ssh, hostname):
    server_info = dict()
    for key, cls in PLUGIN_DICT.items():
        module_path, module_name = cls.rsplit('.', maxsplit=1)
        module = import_module(module_path)
        cls = getattr(module, module_name)
        plugin_obj = cls()
        info = plugin_obj.process(ssh, hostname)
        server_info[key] = info
    return server_info
