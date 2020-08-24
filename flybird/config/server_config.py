# -*- coding: utf-8 -*-

""" 服务端配置
"""

from base.text.conf_reader import ConfReader
from util.common_util import get_file_full_path


class ServerConfig(object):
    """ 服务端配置
    """

    design_doc_path = 'doc'
    server_conf_path = 'conf'

    config_name = None
    current_version = None
    push_red_dot_tip_url = None
    push_red_dot_tip_url_android = None
    celery_config = None
    ios_roll_ip = None
    ios_roll_port = None
    android_roll_ip = None
    android_roll_port = None
    push_kick_message_url_ios = None
    push_kick_message_url_android = None
    log_level = 0

    @classmethod
    def init(cls, config_name=None):
        """ 初始化
        """
        cls.config_name = config_name
        cls.current_version = cls.get_current_version()
        cls.log_level = cls.get_server_info("Base", "log_level", "int")
        cls.push_red_dot_tip_url = cls.get_server_info("Urls", "push_red_dot_tip", 'string')
        cls.push_red_dot_tip_url_android = cls.get_server_info("Urls", "push_red_dot_tip_android", 'string')
        cls.celery_config = cls.get_server_info("Celery")
        cls.ios_roll_ip = cls.get_server_info("IosRoll", 'ip', 'string')
        cls.ios_roll_port = cls.get_server_info("IosRoll", 'port', 'int')
        cls.android_roll_ip = cls.get_server_info("AndroidRoll", 'ip', 'string')
        cls.android_roll_port = cls.get_server_info("AndroidRoll", 'port', 'int')
        cls.push_kick_message_url_ios = cls.get_server_info("Urls", "push_kick_message_ios", "string")
        cls.push_kick_message_url_android = cls.get_server_info("Urls", "push_kick_message_android", "string")

    @staticmethod
    def get_current_version():
        """
        获取当前版本
        :return:
        """
        return ServerConfig.get_server_info(section="Version", field="version", field_type='string')

    @classmethod
    def get_server_info(cls, section, field=None, field_type="string"):
        """
        获得GameDB服务器的ip
        :param section:
        :param field:
        :param field_type:
        :return:
        """
        config_file_name = "{}.conf".format(cls.config_name)
        file_name = get_file_full_path(config_file_name, cls.server_conf_path)
        c = ConfReader()
        c.read(file_name)
        server_info = c.get_field(section, field, field_type)
        return server_info
