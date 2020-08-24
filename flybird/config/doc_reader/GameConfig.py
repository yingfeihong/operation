# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: QL Liu
"""
import sys
from base.text.json_reader import JsonReader
from base.text.xlsx_reader import load_config
from util.common_util import get_file_full_path
from util.singleton import Singleton


class Config(object):
    """
    所有配置
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.item_table = None

    def load_config(self):
        self.item_table = load_config(u"ItemTable-道具表.xlsx")

    @staticmethod
    def load_cmd_config():
        """
        加载cmd
        :return:
        """
        cmd_full_path = get_file_full_path('cmd/cmd.json')
        return JsonReader.read(cmd_full_path)

