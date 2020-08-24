# -*- coding:utf-8 -*-
"""
Module Description:
Date:
Author: QL Liu
"""

import time
import uuid
import requests
import multiprocessing
from base.log.log_manager import LogManager as Log
from base.db.redis_manager import RedisManager
from base.db.db_manager import DBManager
from share import action_status_code as code
from app.constant.admin import LOGIN_ANNOUNCEMENT, MAINTENANCE_ANNOUNCEMENT,\
    ANNOUNCEMENT_FOR_LOGIN, ANNOUNCEMENT_FOR_ROLL, ANNOUNCEMENT_FOR_MAINTAIN,\
    ANNOUNCEMENT_TYPE, CHANNEL_MAP, APP_STORE, ANDROID
from config.server_config import ServerConfig
from base.asyn.celery.task import roll
from app.component.admin_operation_component.limited_author import limited_author


# cmd ：15 type:0,1,5 增 2 删 3 改 4 查
def announcement_do(data):
    author = limited_author(data['user_id'])
    if not author:
        return code.AUTHOR_NOT
    del data['user_id']
    if data:
        if data['type'] == ANNOUNCEMENT_TYPE.ADD_LOGIN:
            return add_login_announcement(data)
        elif data['type'] == ANNOUNCEMENT_TYPE.ADD_MAINTENANCE:
            return add_maintenance_announcement(data)
        elif data['type'] == ANNOUNCEMENT_TYPE.SELECT:
            return announcement_list()
        elif data['type'] == ANNOUNCEMENT_TYPE.DELETE:
            return delete_login_announcement(data)
        elif data['type'] == ANNOUNCEMENT_TYPE.ALTER:
            return alter_login_announcement(data)
        elif data['type'] == ANNOUNCEMENT_TYPE.ADD_ROLL:
            return add_roll_announcement(data)
        else:
            return code.DATA_ERROR
    else:
        return announcement_list()


def add_login_announcement(data):
    """
    添加登入公告
    :param data:
    :return:
    """
    announcement_id = str(uuid.uuid1())
    print "data:", data
    announcement_content = {'content': data['content'], 'announcement_id': announcement_id,
                            'title': data['title'], 'announcement_time': data['announcement_time']}
    result = RedisManager.get_cache(LOGIN_ANNOUNCEMENT, CHANNEL_MAP[data['channel_type']])
    if result:
        result.append(announcement_content)
        RedisManager.cache_set(LOGIN_ANNOUNCEMENT, result, r_type=CHANNEL_MAP[data['channel_type']])
    else:
        result = [announcement_content]
        RedisManager.cache_set(LOGIN_ANNOUNCEMENT, result, r_type=CHANNEL_MAP[data['channel_type']])
    DBManager.insert_record('announcement_record', 'admindb', {'channel_type': data['channel_type'],
                                                               'content': announcement_content,
                                                               'announcement_id': announcement_id,
                                                               'announcement_type': ANNOUNCEMENT_FOR_LOGIN,
                                                               'create_time': time.time()})
    return code.OK


def add_roll_announcement(data):
    """
    发送滚动公告
    :param data:
    :return:
    """
    if data['channel_type'] == APP_STORE:
        roll_ip = ServerConfig.ios_roll_ip
        roll_port = ServerConfig.ios_roll_port
    elif data['channel_type'] == ANDROID:
        roll_ip = ServerConfig.android_roll_ip
        roll_port = ServerConfig.android_roll_port
    else:
        return code.DATA_ERROR
    print '开始滚动公告'
    roll_p = multiprocessing.Process(target=roll_send, args=(data['content'],
                                                             data['number_of_time'], roll_ip, roll_port))
    # roll_p.daemon = True
    roll_p.start()
    DBManager.insert_record('announcement_record', 'admindb', {'channel_type': data['channel_type'],
                                                               'content': data['content'],
                                                               'announcement_type': ANNOUNCEMENT_FOR_ROLL,
                                                               'create_time': time.time()})
    return code.OK


def roll_send(content, roll_time, roll_ip, roll_port):
    """
    发送滚动公告
    :param content:
    :param roll_time:
    :param roll_ip:
    :param roll_port:
    :return:
    """
    for roll in range(roll_time):
        try:
            requests.post('http://{}:{}/announcement/add'.format(roll_ip, roll_port),
                          json={'content': content})
            time.sleep(300)
        except Exception as e:
            Log.logger.info("add roll announcement fail, error is {}".format(e))


def add_maintenance_announcement(data):
    """
    发送运维公告
    :param data:
    :return:
    """
    content = data['content']
    end_time = data['endTime']
    if end_time <= time.time():
        return code.END_TIME_SHOULD_BE_GREATER_THAN_START_TIME
    if not content:
        return code.ANNOUNCEMENT_CONTENT_NOT_BE_NULL
    maintenance_info = {'content': content, 'end_time': end_time}
    expire_time = int(end_time-time.time())
    Log.logger.info("add_maintenance_announcement, expire time:{}s".format(expire_time))
    Log.logger.info('运维公告发布')
    RedisManager.cache_set(MAINTENANCE_ANNOUNCEMENT, maintenance_info, expire_time,
                           r_type=CHANNEL_MAP[data['channel_type']])
    DBManager.insert_record('announcement_record', 'admindb', {'channel_type': data['channel_type'],
                                                               'content': maintenance_info,
                                                               'announcement_type': ANNOUNCEMENT_FOR_MAINTAIN,
                                                               'create_time': time.time()})

    return code.OK


def announcement_list():
    """
    获取公告列表
    :return:
    """
    result = []
    for content in DBManager.get_multi_record('announcement_record', 'admindb'):
        del content['_id']
        result.append(content)
    return {'data': result}


def delete_login_announcement(data):
    """
    删除公告
    :return:
    """
    result = RedisManager.get_cache(LOGIN_ANNOUNCEMENT, CHANNEL_MAP[data['channel_type']])
    if result:
        for i in result:
            for key in i.keys():
                if key == 'announcement_id':
                    if i['announcement_id'] == data['announcement_id']:
                        result.remove(i)
                        DBManager.delete_record('announcement_record', 'admindb', {'content': i})
        RedisManager.cache_set(LOGIN_ANNOUNCEMENT, result, r_type=CHANNEL_MAP[data['channel_type']])
        return code.ANNOUNCEMENT_DELETE
    else:
        return code.ANNOUNCEMENT_NOT_EXIST


def alter_login_announcement(data):
    """
    修改公告内容
    :param data:
    :return:
    """
    announcement = RedisManager.get_cache(LOGIN_ANNOUNCEMENT, CHANNEL_MAP[data['channel_type']])
    if not announcement:
        return code.ANNOUNCEMENT_NOT_EXIST
    alter_field = {1: 'title', 2: 'content', 3: 'announcement_time'}
    for i in announcement:
        for key in i.keys():
            if key == 'announcement_id':
                if i['announcement_id'] == data['announcement_id']:
                    i[alter_field[data['up_data']]] = data['content']
                    DBManager.update_property('announcement_record', 'admindb',
                                              {'announcement_id': data['announcement_id']},
                                              'content', i)
    RedisManager.cache_set(LOGIN_ANNOUNCEMENT, announcement, r_type=CHANNEL_MAP[data['channel_type']])
    return code.ANNOUNCEMENT_UPDATE


