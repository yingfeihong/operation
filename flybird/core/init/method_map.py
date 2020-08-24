# -*- coding:utf-8 -*-
"""
Module Description: cmd映射处理
Date: 2018-3-29
Author: QL Liu
"""
import os
import logging
from config.doc_reader.GameConfig import Config


class MethodMap(object):

    map_classes = dict()
    cmd_config = None

    @classmethod
    def map_method(cls):
        cls.cmd_config = Config.load_cmd_config()
        cls.deal_cmd_map_class()

    @classmethod
    def deal_cmd_map_class(cls):
        """
        cmd映射处理类
        :return:
        """
        modules = []
        for filename in os.listdir('app/action'):
            if filename.endswith('py') and filename.startswith('act'):
                module_name = "app.action.{}".format(filename[:-3])
                modules.append(__import__(module_name, fromlist=True))
        for class_name, cmd in cls.cmd_config.items():
            for module in modules:
                class_address = getattr(module, class_name, None)
                if class_address:
                    cls.map_classes[cmd] = class_address


