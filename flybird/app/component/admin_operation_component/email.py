# -*- coding:utf-8 -*-
"""
Module Description:
Date:
Author: QL Liu
"""

import uuid
import time
from base.db.db_manager import DBManager
from base.asyn.celery.task import update_email_data, update_email_data_android,\
    push_email_red_tip, push_email_red_tip_android
from share import action_status_code as code
from config.doc_reader.GameConfig import Config
from app.constant.admin import EMAIL_TYPE, CHANNEL_MAP_DB, IOS_GAME, SURPLUS_TIME
from base.log.log_manager import LogManager as Log
from app.component.admin_operation_component.limited_author import limited_author


# cmd ：16
def email(data):
    author = limited_author(data['user_id'])
    if not author:
        return code.AUTHOR_NOT
    del data['user_id']
    if data:
        if data['type'] == EMAIL_TYPE.SEND:  # 发送邮件
            return send_email_reward(data)
        elif data['type'] == EMAIL_TYPE.DELETE:  # 删除邮件
            return deal_email_del(data)
        elif data['type'] == EMAIL_TYPE.GET:  # 获取邮件列表
            return get_email_list()
        else:
            return code.DATA_ERROR
    else:
        return get_email_list()


def send_email_reward(data):
    """
    发送邮件奖励
    :param data:
    :return:
    """
    is_all = data['is_all']
    title = data['title']
    content = data['content']
    email_type = data['email_type']
    # 遍历道具
    for _item in data['item_list']:
        if _item[0] not in Config().item_table:
            Log.logger.info('not exist item:{}, type:{}'.format(_item[0], type(_item[0])))
            return code.ITEM_NOT_FOUND
    # 判断邮件类型 TODO 邮件类型应以客户端上传为准，依靠itemList来判定不好
    email_id = str(uuid.uuid1())
    # 判断是单人还是全体
    if not is_all:  # 个人
        role = DBManager.get_record('role_data', CHANNEL_MAP_DB[data['channel_type']], {'role_name': data['role_id']})
        if not role:
            return code.ROLE_NOT_EXIT
        role_id = str(role['_id'])
        if CHANNEL_MAP_DB[data['channel_type']] == IOS_GAME:
            update_email_data_for_one(role_id, email_id, email_type, data['item_list'], title, content, data)
        else:
            update_email_data_for_one_android(role_id, email_id, email_type, data['item_list'], title, content, data)
        return code.OK
    else:  # 全部
        if CHANNEL_MAP_DB[data['channel_type']] == IOS_GAME:
            print '苹果邮件群发'
            update_email_data.delay(email_id, email_type,
                                    data['item_list'], title, content, data)
        else:
            print '安卓邮件群发'
            update_email_data_android.delay(email_id, email_type,
                                            data['item_list'], title, content, data)
        return code.OK


def deal_email_del(data):
    """
    删除邮件
    :param data:
    :return:
    """
    primary_id = data['primary_id']
    DBManager.delete_record('email_record', 'admindb', {'primaryId': primary_id})
    DBManager.delete_record('email_record_all', 'admindb', {'primaryId': primary_id}, multi=True)
    return code.OK


def get_email_list():
    """
    获取邮件列表
    :param :
    :return:
    """
    result = []
    for content in DBManager.get_multi_record('email_record', 'admindb'):
        del content['_id']
        result.append(content)
    return {'data': result}


def update_email_data_for_one(role_id, email_id, email_type, item_reward, title, content, data):
    """
    新建一个邮件
    :param role_id:
    :param email_id:
    :param email_type:
    :param item_reward:
    :param title:
    :param content:
    :param data:
    :return:
    """
    temp_email = {"title": title,
                  "content": content,
                  "surplus_time": SURPLUS_TIME,
                  "item_reward": item_reward, "type": email_type,
                  "status": 0, "get_time": int(time.time())}

    email_data = DBManager.get_record('email_data', CHANNEL_MAP_DB[data['channel_type']], {"role_id": role_id})
    email_list = dict() if not email_data else email_data["email_list"]
    email_list[email_id] = temp_email
    if not email_data:
        email_data = {"role_id": role_id, "email_list": email_list}
        DBManager.insert_record("email_data", CHANNEL_MAP_DB[data['channel_type']], email_data)
    else:
        DBManager.update_property("email_data", CHANNEL_MAP_DB[data['channel_type']], {"role_id": role_id},
                                  "email_list", email_list)
    push_email_red_tip(role_id, False)
    if not DBManager.get_record('email_record', 'admindb', {'primaryId': email_id}):
        DBManager.insert_record('email_record', 'admindb', {'primaryId': email_id, 'is_all': data['is_all'],
                                                            'role_id': [data['role_id']], 'title': title,
                                                            'create_time': time.time(),
                                                            'content': content, 'email_type': email_type,
                                                            'item_list': data['item_list'],
                                                            'channel_type': data['channel_type']})
    else:
        role_id_list = DBManager.get_record('email_record', 'admindb', {'primaryId': email_id})['role_id']
        role_id_list.append(role_id)
        DBManager.update_property('email_record', 'admindb', {'primaryId': email_id}, 'role_id', role_id_list)
    return True


def update_email_data_for_one_android(role_id, email_id, email_type, item_reward, title, content, data):
    """
    新建一个邮件
    :param role_id:
    :param email_id:
    :param email_type:
    :param item_reward:
    :param title:
    :param content:
    :param data:
    :return:
    """
    temp_email = {"title": title,
                  "content": content,
                  "surplus_time": SURPLUS_TIME,
                  "item_reward": item_reward, "type": email_type,
                  "status": 0, "get_time": int(time.time())}

    email_data = DBManager.get_record('email_data', CHANNEL_MAP_DB[data['channel_type']], {"role_id": role_id})
    email_list = dict() if not email_data else email_data["email_list"]
    email_list[email_id] = temp_email
    if not email_data:
        email_data = {"role_id": role_id, "email_list": email_list}
        DBManager.insert_record("email_data", CHANNEL_MAP_DB[data['channel_type']], email_data)
    else:
        DBManager.update_property("email_data", CHANNEL_MAP_DB[data['channel_type']], {"role_id": role_id},
                                  "email_list", email_list)
    push_email_red_tip_android(role_id, False)
    if not DBManager.get_record('email_record', 'admindb', {'primaryId': email_id}):
        DBManager.insert_record('email_record', 'admindb', {'primaryId': email_id, 'is_all': data['is_all'],
                                                            'role_id': [data['role_id']], 'title': title,
                                                            'create_time': time.time(),
                                                            'content': content, 'email_type': email_type,
                                                            'item_list': data['item_list'],
                                                            'channel_type': data['channel_type']})
    else:
        role_id_list = DBManager.get_record('email_record', 'admindb', {'primaryId': email_id})['role_id']
        role_id_list.append(role_id)
        DBManager.update_property('email_record', 'admindb', {'primaryId': email_id}, 'role_id', role_id_list)
    return True
