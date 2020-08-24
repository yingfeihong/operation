# -*- coding:utf-8 -*-
"""
Module Description:
Date:
Author: QL Liu
"""

import time
from share import action_status_code as code
from base.db.db_manager import DBManager
from bson import ObjectId
from app.constant.admin import BAN_TYPE, STATUS_TYPE, ANDROID, APP_STORE
from app.component.admin_operation_component.limited_author import limited_author
from base.db.redis_manager import RedisManager
from config.server_config import ServerConfig


# cmd ：17
def set_account_status(data):
    """
    设置账户状态
    :param data:
    :return:
    """
    author = limited_author(data['user_id'])
    if not author:
        return code.AUTHOR_NOT
    del data['user_id']
    if data:
        if data['set_status'] == STATUS_TYPE.BAN:
            if data['type'] == BAN_TYPE.BAN:
                ban = data['ban']
                account = data['account']
                if data['channel_type'] == 'appstore':
                    role = DBManager.get_record('role_data', 'iosgame', {'role_name': account})
                    if not role:
                        return code.ROLE_NOT_EXIT
                    user_info = DBManager.get_record("account_info", 'iosgame', {'_id': ObjectId(role['user_id'])})
                    user_status = user_info.get('ban')
                    if ban and user_status == ban:
                        return code.THE_USER_HAS_BEEN_BAN_STATUS
                    DBManager.update_property("account_info", 'iosgame',  {'_id': ObjectId(role['user_id'])},
                                              'ban', ban)
                    if ban:
                        import requests
                        try:
                            requests.post(ServerConfig.push_kick_message_url_ios,
                                          json={'status_code': code.ACCOUNT_IN_BAN_STATUS,
                                                'is_all': False, 'role_id': str(role['_id'])})
                        except Exception as e:
                            print e
                            return code.FAIL
                        # 移除排行榜
                        RedisManager.ios_r.zrem("rank:competitive:name", str(role['_id']))
                        RedisManager.ios_r.zrem("legend:rank:name", str(role['_id']))
                    if not DBManager.get_record('ban_record', 'admindb', {'role': account}):
                        DBManager.insert_record('ban_record', 'admindb', {'role': account, 'ban_time': time.time(),
                                                                          'ban_info': data['content'], 'stasus': ban,
                                                                          'channel_type': data['channel_type']})
                    else:
                        DBManager.update_one('ban_record', 'admindb', {'role': account},
                                             {'role': account, 'ban_time': time.time(),
                                             'ban_info': data['content'], 'stasus': ban,
                                              'channel_type': data['channel_type']})
                    return code.OK
                else:
                    role = DBManager.get_record('role_data', 'androidgame', {'role_name': account})
                    if not role:
                        return code.ROLE_NOT_EXIT
                    user_info = DBManager.get_record("account_info", 'androidgame', {'_id': ObjectId(role['user_id'])})
                    user_status = user_info.get('ban')
                    if ban and user_status == ban:
                        return code.THE_USER_HAS_BEEN_BAN_STATUS
                    DBManager.update_property("account_info", 'androidgame', {'_id': ObjectId(role['user_id'])},
                                              'ban', ban)
                    if ban:
                        import requests
                        try:
                            requests.post(ServerConfig.push_kick_message_url_android,
                                          json={'status_code': code.ACCOUNT_IN_BAN_STATUS,
                                                'is_all': False, 'role_id': str(role['_id'])})
                        except Exception as e:
                            print e
                            return code.FAIL
                        # 移除排行榜
                        RedisManager.android_r.zrem("rank:competitive:name", str(role['_id']))
                        RedisManager.android_r.zrem("legend:rank:name", str(role['_id']))
                    if not DBManager.get_record('ban_record', 'admindb', {'role': account}):
                        DBManager.insert_record('ban_record', 'admindb', {'role': account, 'ban_time': time.time(),
                                                                          'ban_info': data['content'], 'stasus': ban,
                                                                          'channel_type': data['channel_type']})
                    else:
                        DBManager.update_one('ban_record', 'admindb', {'role': account},
                                             {'role': account, 'ban_time': time.time(),
                                              'ban_info': data['content'], 'stasus': ban,
                                              'channel_type': data['channel_type']})
                    return code.OK
            else:
                result = DBManager.get_record('ban_record', 'admindb', {'role': data['account']})
                if not result:
                    return code.ROLE_NOT_EXIT
                del result['_id']
                return {'data': result}
        else:
            channel = data['channel_name']
            role_name = data['role_name']
            set_type = data['set_type']
            expire_time = data['expire_time']
            content = data['content']
            if channel == APP_STORE:
                role = DBManager.get_record('role_data', 'iosgame', {'role_name': role_name})
                if not role:
                    return code.USER_NOT_EXIST
                key = "forbidden:word:{}".format(str(role['_id']))
                if set_type == 0:
                    if expire_time != -1:
                        RedisManager.cache_set(key=key, value=1, expire=expire_time*3600, r_type='ios')
                    else:
                        RedisManager.cache_set(key=key, value=1, r_type='ios')
                else:
                    RedisManager.delete_key(key, r_type='ios')
                result = {'channel_type': channel, 'ban_time': expire_time,
                          'role_name': role_name, 'set_type': set_type, 'content': content}
                if not DBManager.get_record('talk_record', 'admindb', {'role_name': role_name}):
                    DBManager.insert_record('talk_record', 'admindb', result)
                else:
                    DBManager.update_one('talk_record', 'admindb', {'role_name': role_name}, result)
                return code.OK
            elif channel == ANDROID:
                role = DBManager.get_record('role_data', 'androidgame', {'role_name': role_name})
                if not role:
                    return code.USER_NOT_EXIST
                key = "forbidden:word:{}".format(str(role['_id']))
                if set_type == 0:
                    if expire_time != -1:
                        RedisManager.cache_set(key=key, value=1, expire=expire_time*3600, r_type='android')
                    else:
                        RedisManager.cache_set(key=key, value=1, r_type='android')
                else:
                    RedisManager.delete_key(key, r_type='android')
                result = {'channel_type': channel, 'ban_time': expire_time,
                          'role_name': role_name, 'set_type': set_type, 'content': data['content']}

                if not DBManager.get_record('talk_record', 'admindb', {'role_name': role_name}):
                    DBManager.insert_record('talk_record', 'admindb', result)
                else:
                    DBManager.update_one('talk_record', 'admindb', {'role_name': role_name}, result)
                return code.OK
            else:
                return code.ARGS_ERROR
    else:
        result_ban = []
        result_talk = []
        for content in DBManager.get_multi_record('ban_record', 'admindb'):
            del content['_id']
            result_ban.append(content)
        for content in DBManager.get_multi_record('talk_record', 'admindb'):
            del content['_id']
            result_talk.append(content)
        return {'data': [result_ban, result_talk]}


def battle_error(data):
    """
    分页显示作弊名单
    :param data:
    :return:
    """
    skip_number = data.get('skip')
    if skip_number:
        skip = 30 * int(skip_number) - 30
    else:
        skip = 0
    result = list()
    if data.get('channel_type') == 'appstore':
        all_number = DBManager.get_multi_record_count('battle_error_data', 'iosgame',
                                                      {'fight_type': data.get('battle_type'),
                                                       'number': {'$gte': data['number']}})
        all_number = all_number//30 if all_number % 30 == 0 else all_number//30 + 1
        roles = DBManager.get_multi_record_limit('battle_error_data', 'iosgame',
                                                 {'fight_type': data.get('battle_type'),
                                                  'number': {'$gte': data['number']}}, limit=30, skip=skip)
        for role in roles:
            role_name = DBManager.get_record('role_data', 'iosgame',
                                             {'_id': ObjectId(str(role['role_id']))})['role_name']
            number = role['number']
            result.append({'role_name': role_name, 'number': number})
    else:
        all_number = DBManager.get_multi_record_count('battle_error_data', 'androidgame',
                                                      {'fight_type': data.get('battle_type'),
                                                       'number': {'$gte': data['number']}})
        all_number = all_number // 30 if all_number % 30 == 0 else all_number // 30 + 1
        roles = DBManager.get_multi_record_limit('battle_error_data', 'androidgame',
                                                 {'fight_type': data.get('battle_type'),
                                                  'number': {'$gte': data['number']}}, limit=30, skip=skip)
        for role in roles:
            role_name = DBManager.get_record('role_data', 'androidgame',
                                             {'_id': ObjectId(str(role['role_id']))})['role_name']
            number = role['number']
            result.append({'role_name': role_name, 'number': number})
    return {'data': result, 'all_number': all_number}


