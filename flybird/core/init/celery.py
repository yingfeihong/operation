# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: QL Liu
"""
from base.db.db_util import DBUtil
from base.log.log_manager import LogManager
from base.db.redis_manager import RedisManager
from config.server_config import ServerConfig
from core.init.config_loader import ConfigLoader


class CeleryServerInit(object):
    """ 初始化: LogServer
    """

    @classmethod
    def init(cls, config_name):
        """ 初始化
        """

        # 服务器基本配置初始化
        ServerConfig.init(config_name)

        # 日志服务初始化
        LogManager.init()

        # 缓存初始化
        RedisManager()

        # 加载所有策划文档
        ConfigLoader.load_all_configs()

        # # 数据库初始化
        DBUtil.init()
