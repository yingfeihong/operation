# -*- coding: utf-8 -*-

""" 数据库管理类
"""
from pymongo import MongoClient
from config.server_config import ServerConfig


class DBUtil(object):
    """ 数据库管理类
    """

    db_connection = None  # 数据库链接 (DB)
    game1_db_connection = None  # 游戏数据库链接 (GameDB)
    game2_db_connection = None  # 3月份测试玩家数据库连接
    game3_db_connection = None  # 6月份测试玩家数据连接
    ios_db_connection = None  # ios
    android_db_connection = None  # android

    @classmethod
    def init(cls):
        """
        初始化
        :return:
        """
        cls.db_connection = cls.connect_db('admindb', 'DBServer')
        cls.game1_db_connection = cls.connect_db('game', 'GameDBServer')
        cls.game2_db_connection = cls.connect_db('game', 'TestDBServer')
        cls.game3_db_connection = cls.connect_db('game', 'TestOneDBServer')
        cls.ios_db_connection = cls.connect_db('game', 'IosDBServer')
        cls.android_db_connection = cls.connect_db('game', 'AndroidDBServer')
    @classmethod
    def connect_db(cls, db_name, section):

        """
        连接GameDB数据库
        :param db_name:
        :param section:
        :return:
        """
        from base.log.log_manager import LogManager as Log
        field_address = "address"
        field_user = "user"
        field_password = "password"
        field_auth = "auth"
        field_replicat_set = "replicat_set"
        field_replicat_name = "replicat_name"

        db_address = ServerConfig.get_server_info(section, field_address)
        print db_address

        Log.logger.info("db_address:{}".format(db_address))
        user = ServerConfig.get_server_info(section, field_user)

        password = ServerConfig.get_server_info(section, field_password)

        auth = ServerConfig.get_server_info(section, field_auth, "boolean")
        address_list = db_address.split('|')

        replicat_set = ServerConfig.get_server_info(section, field_replicat_set, "boolean")

        if replicat_set:
            replicat_name = ServerConfig.get_server_info(section, field_replicat_name)
            client = MongoClient(address_list, replicaSet=replicat_name)
        else:
            client = MongoClient(address_list)

        db_auth = client[db_name]
        print db_auth
        if auth:
            print "auth:", auth, user, password
            db_auth.authenticate(user, password)

        return client

    @classmethod
    def get_db_connection(cls, db_name):

        """
        获得数据库连接
        :return:
        """
        db_map = {
            'admindb': cls.db_connection['admindb'],
            'game1': cls.game1_db_connection['game'],
            'game2': cls.game2_db_connection['game'],
            'game3': cls.game3_db_connection['game'],
            'iosgame': cls.ios_db_connection['game'],
            'androidgame': cls.android_db_connection['game']
        }
        return db_map.get(db_name)

    @classmethod
    def get_db_instance(cls, db_name):
        """
        根据表名获取db实例
        :param db_name:
        :return:
        """
        return DBUtil.get_db_connection(db_name)

