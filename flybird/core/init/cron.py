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


class CronServerInit(object):
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

        # 数据库初始化
        DBUtil.init()






