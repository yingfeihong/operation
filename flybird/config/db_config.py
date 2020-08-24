# -*- coding: utf-8 -*-

""" 数据库配置
"""


class DBConfig(object):
    """ 数据库配置
    """

    design_doc_path = 'doc'
    server_conf_path = 'conf'
    config_name = None

    @classmethod
    def init(cls, config_name=None):
        """ 初始化
        """
        cls.config_name = config_name
