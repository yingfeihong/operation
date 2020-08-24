# -*- coding:utf-8 -*-
"""
Module Description:
Date:
Author: QL Liu
"""

from share import action_status_code as code
import requests
from base.db.redis_manager import RedisManager
from app.constant.admin import MAX_CIRCULATE_NUM, SERVER_STATUS_KEY, IOS_GAME, \
    ANDROID_GAME
from config.server_config import ServerConfig
from base.log.log_manager import LogManager as Log


# cmd ：18
def set_server_status(data):
    """
    设置服务器状态
    :return:
    """
    status = data['status']
    version = data['version']
    channel_type = data['channel_type']
    if status:  # 关服
        error = update_server_status(version, status, channel_type)
        if not error:
            return code.CLOSE_SERVER_FAIL
        try:
            if channel_type == IOS_GAME:
                requests.post(ServerConfig.push_kick_message_url, json={'status_code': code.SEVER_IN_MAINTENANCE,
                                                                        'is_all': True})
        except Exception as e:
            Log.logger.error("push kick message fail, error:{}".format(e))
            return code.OK
    else:  # 开服
        error = update_server_status(version, status, channel_type)
        if not error:
            return code.CLOSE_SERVER_FAIL


def update_server_status(data, status, channel_type):
    """
    更新服务器状态
    :return:
    """
    current_version = float(data)
    if current_version < 1:
        return False
    circulate_num = 0
    while True:
        if circulate_num > MAX_CIRCULATE_NUM:
            return
        if current_version <= 0.9:
            return True
        key = SERVER_STATUS_KEY.format(current_version)
        print "key:", key
        if channel_type == IOS_GAME:
            if status:
                RedisManager.ios_r.set(key, status)
            else:
                RedisManager.delete_keys(key, r_type='ios')
        elif channel_type == ANDROID_GAME:
            if status:
                RedisManager.android_r.set(key, status)
            else:
                RedisManager.delete_keys(key, r_type='android')
        else:
            pass
        current_version -= 0.1
        circulate_num += 1





