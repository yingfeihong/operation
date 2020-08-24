# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: QL Liu
"""
import requests
import time
from base.db.db_manager import DBManager
from celeryapp import app
from app.constant.admin import SURPLUS_TIME
from app.constant.admin import RED_DOT_TIP, CHANNEL_MAP_DB
from config.server_config import ServerConfig
from base.log.log_manager import LogManager as Log
from share import action_status_code as code


@app.task
def update_email_data(email_id, email_type, item_reward, title, content, data):
    """
    新建一个邮件
    :param email_id:
    :param email_type:
    :param item_reward:
    :param title:
    :param content:
    :return:
    """
    role_list = DBManager.get_multi_record("role_data", CHANNEL_MAP_DB[data['channel_type']], {})
    temp_email = {"title": title,
                  "content": content,
                  "surplus_time": SURPLUS_TIME,
                  "item_reward": item_reward, "type": email_type,
                  "status": 0, "get_time": int(time.time())}
    email_record = DBManager.get_record('email_record', 'admindb', {'primaryId': email_id})
    if not email_record:
        DBManager.insert_record('email_record', 'admindb', {'primaryId': email_id, 'is_all': data['is_all'],
                                                            'role_id': '', 'title': title,
                                                            'create_time': time.time(),
                                                            'content': content, 'email_type': email_type,
                                                            'item_list': data['item_list'],
                                                            'channel_type': data['channel_type']})
    for role in role_list:
        role_id = str(role['_id'])
        email_data = DBManager.get_record('email_data', CHANNEL_MAP_DB[data['channel_type']], {"role_id": role_id})
        email_list = dict() if not email_data else email_data["email_list"]
        email_list[email_id] = temp_email
        if not email_data:
            email_data = {"role_id": role_id, "email_list": email_list}
            DBManager.insert_record("email_data", CHANNEL_MAP_DB[data['channel_type']], email_data)
        else:
            DBManager.update_property("email_data", CHANNEL_MAP_DB[data['channel_type']], {"role_id": role_id},
                                      "email_list", email_list)
        DBManager.insert_record('email_record_all', 'admindb', {'primaryId': email_id, 'role_id': role_id})
    role_id = ''
    push_email_red_tip(role_id, data['is_all'])
    return True


@app.task
def update_email_data_android(email_id, email_type, item_reward, title, content, data):
    """
    新建一个邮件
    :param email_id:
    :param email_type:
    :param item_reward:
    :param title:
    :param content:
    :return:
    """
    role_list = DBManager.get_multi_record("role_data", CHANNEL_MAP_DB[data['channel_type']], {})
    temp_email = {"title": title,
                  "content": content,
                  "surplus_time": SURPLUS_TIME,
                  "item_reward": item_reward, "type": email_type,
                  "status": 0, "get_time": int(time.time())}
    email_record = DBManager.get_record('email_record', 'admindb', {'primaryId': email_id})
    if not email_record:
        DBManager.insert_record('email_record', 'admindb', {'primaryId': email_id, 'is_all': data['is_all'],
                                                            'role_id': '', 'title': title,
                                                            'create_time': time.time(),
                                                            'content': content, 'email_type': email_type,
                                                            'item_list': data['item_list'],
                                                            'channel_type': data['channel_type']})
    for role in role_list:
        role_id = str(role['_id'])
        email_data = DBManager.get_record('email_data', CHANNEL_MAP_DB[data['channel_type']], {"role_id": role_id})
        email_list = dict() if not email_data else email_data["email_list"]
        email_list[email_id] = temp_email
        if not email_data:
            email_data = {"role_id": role_id, "email_list": email_list}
            DBManager.insert_record("email_data", CHANNEL_MAP_DB[data['channel_type']], email_data)
        else:
            DBManager.update_property("email_data", CHANNEL_MAP_DB[data['channel_type']], {"role_id": role_id},
                                      "email_list", email_list)
        DBManager.insert_record('email_record_all', 'admindb', {'primaryId': email_id, 'role_id': role_id})
    role_id = ''
    push_email_red_tip_android(role_id, data['is_all'])
    return True


def push_email_red_tip(role_id, is_all):
    """
    推送红点消息给客户端
    :param role_id:
    :param is_all:
    :return:
    """
    data = {'role_id': role_id, 'is_all': is_all, 'message_type': [RED_DOT_TIP.EMAIL]}
    try:
        requests.post(ServerConfig.push_red_dot_tip_url, json=data)
    except Exception as e:
        Log.logger.error("push email red tip fail, error is {}".format(e))
        return False
    return True


def push_email_red_tip_android(role_id, is_all):
    """
    推送红点消息给客户端
    :param role_id:
    :param is_all:
    :return:
    """
    data = {'role_id': role_id, 'is_all': is_all, 'message_type': [RED_DOT_TIP.EMAIL]}
    try:
        requests.post(ServerConfig.push_red_dot_tip_url_android, json=data)
    except Exception as e:
        Log.logger.error("push email red tip fail, error is {}".format(e))
        return False
    return True


@app.task
def roll(roll_ip, roll_port, data):
    for roll_time in range(data['number_of_time']):
        try:
            requests.post('http://{}:{}/announcement/add'.format(roll_ip, roll_port),
                          json={'content': data['content']})
            time.sleep(300)
        except Exception as e:
            Log.logger.info("add roll announcement fail, error is {}".format(e))
            return code.ROLL_FAILED

