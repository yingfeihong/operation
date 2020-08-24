# -*- coding: utf-8 -*-

""" 游戏日志
"""
import logging
import colorlog
import logging.handlers
from datetime import datetime
from base.db.db_manager import DBManager
from config.server_config import ServerConfig


class LogManager(object):
    """ 游戏日志
    包含对运营日志、系统日志、错误日志的处理
    """
    logger = None  # 系統錯誤日誌

    @classmethod
    def init(cls):
        """
        初始化
        :return:
        """
        cls.logger = Logger()

    @staticmethod
    def create_log_dict(user_id, action, content, date, time):
        """
        生成日志结构体
        :param user_id:
        :param action:
        :param content:
        :param date:
        :param time:
        :return:
        """
        log_dict ={
            "user_id": user_id,
            "action": action,
            "content": content,
            "date": date,
            "time": time
        }
        return log_dict

    @classmethod
    def write(cls, user_id, action, content):
        """
        日志写入数据库
        :param user_id:
        :param action:
        :param content: 该字段不设置默认空值的原因是，强制记录一些对游戏分析有用的数据
        :return:
        """
        # 获取时间
        now = datetime.now()
        now_str = str(now)
        time_str_list = now_str.split(" ")
        date = time_str_list[0]
        time = time_str_list[1]

        # 生成新的表名      (如果该表不存在，则根据数据库的机制，会自动创建一个新的表)
        table = "log_" + date

        # 生成日志结构体
        record = cls.create_log_dict(user_id, action, content, date, time)

        # 插入数据库  Todo 此处应该发给消息队列已提高性能并且解耦，不能直接入库
        DBManager.insert_record(table, record)


class Logger(logging.Logger):

    def __init__(self):
        super(Logger, self).__init__(self)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        log_format = '\n'.join((
            '/' + '-' * 80,
            '[%(levelname)s][%(asctime)s][%(process)d:%(thread)d][%(filename)s:%(lineno)d %(funcName)s]:',
            '%(message)s',
            '-' * 80 + '/',
        ))
        color_log_format = '%(log_color)s' + log_format
        console_handler.setFormatter(colorlog.ColoredFormatter(color_log_format, log_colors={
            'DEBUG': 'white',
            'INFO': 'yellow',
            'WARNING': 'blue',
            'ERROR': 'red',
            'CRITICAL': 'red',
        }))
        console_handler.setLevel(ServerConfig.log_level)
        self.addHandler(console_handler)