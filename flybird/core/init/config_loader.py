# -*- coding: utf-8 -*-

""" 配置加载
"""

from config.doc_reader.GameConfig import Config


class ConfigLoader(object):
    """ 配置加载
    """

    @classmethod
    def load_all_configs(cls):
        """
        加载所有的游戏策划的配置表
        :return:
        """
        Config().load_config()

    @classmethod
    def load_configs_for_gate_sever(cls):
        """
        加载所有的GateServer的配置表
        :return:
        """
        # csv格式的文件
        pass

