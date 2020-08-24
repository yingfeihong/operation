# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: QL Liu
"""

from tornado.web import Application
from base.db.db_util import DBUtil
from base.db.redis_manager import RedisManager
from base.log.log_manager import LogManager
from config.db_config import DBConfig
from config.server_config import ServerConfig
from core.init.method_map import MethodMap
from router.admin_router import AdminRouter
from core.init.config_loader import ConfigLoader


class AdminServerInit(object):
    """ 初始化: AccountServer
    """
    handler_list = []  # 响应函数的列表

    @classmethod
    def init(cls, config_name):
        """ 初始化
        """
        # 服务器基本配置初始化
        ServerConfig.init(config_name)

        # 日志服务初始化
        LogManager.init()

        # 数据库基本配置初始化
        DBConfig.init(config_name)

        # 数据库初始化
        DBUtil.init()

        # Redis 缓存初始化
        RedisManager()

        # 加载所有策划文档
        ConfigLoader.load_all_configs()

        # cmd 映射
        MethodMap.map_method()
        # 请求响应模块初始化
        cls.init_router()

    @classmethod
    def get_handler_list(cls):
        """
        获取所有的请求响应的函数的集合
        :return application:
        """
        return Application(cls.handler_list)

    @classmethod
    def init_router(cls):
        """ 初始化
        """
        AdminRouter.add_handler(cls.handler_list)            # 账户
