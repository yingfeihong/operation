# -*- coding: utf-8 -*-

""" 读取Json文件
"""

import json


class JsonReader(object):
    """ 读取Json文件
    """

    @classmethod
    def read(cls, file_name):
        """
        读取文件
        :param file_name: csv文件名
        :return:
        """
        doc = json.load(file(file_name))
        return doc


