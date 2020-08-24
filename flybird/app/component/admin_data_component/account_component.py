# -*- coding:utf-8 -*-
"""
Module Description:
Date: 2018-12-25
Author: QL Liu
"""
from base.db.db_manager import DBManager
from config.db.DbTableConfig import DbTableConfig
from app.constant import account as constant
from base.encrypt.encrypt import encrypt_md5
from base.authentication.authentication import verify_token, generate_token
from share import action_status_code as code
from base.log.log_manager import LogManager as Log


# cmd ：1
def create_account(account, password, account_type):
    """
    临时创建管理用户
    :param account:
    :param password:
    :param account_type:
    :return:
    """
    account_info = DBManager.get_record(DbTableConfig.table_admin_account, {'account': account})
    if account_info:
        return code.THE_ACCOUNT_EXIST
    if account_type == constant.ACCOUNT_TYPE.COMMON:
        account_info = DBManager.get_record(DbTableConfig.table_admin_account,
                                            {'account_type': constant.ACCOUNT_TYPE.COMMON})
        if account_info:
            return code.ROOT_ACCOUNT_CAN_ONLY_HAVE_ONE
    encrypt_password = encrypt_md5(str(password))
    DBManager.insert_record(DbTableConfig.table_admin_account, {'account': account,
                                                                'password': encrypt_password,
                                                                'account_type': account_type})
    return {'msg': 'successful'}


# cmd ：2
def login(account, password):
    """
    登录
    :param account:
    :param password:
    :return:
    """

    account_info = DBManager.get_record('admin_account', 'admindb', {'account': account})
    if not account_info:
        return code.USER_NOT_EXIST
    Log.logger.info(password)
    encrypt_password = encrypt_md5(str(password))
    if encrypt_password != account_info['password']:
        return code.PASSWORD_ERROR
    user_id = str(account_info['_id'])
    access_token = generate_token(user_id, 'access')
    refresh_token = generate_token(user_id, 'refresh')
    if account_info['account_type'] == 1:
        return {'account_type': 1, 'accessToken': access_token, 'refreshToken': refresh_token, 'user_id': user_id}
    else:
        channel_list_dic = []
        for channel_list in account_info['channel_list']:
            channel_all = DBManager.get_record('channel_all', 'admindb', {'big_channel': channel_list})
            if channel_all:
                channel_list_dic.append({channel_list: channel_all['channel_list']})

        if 'show' in account_info:
            return {'accessToken': access_token, 'refreshToken': refresh_token,
                    'gameList': account_info['game_list'],
                    'channelList': channel_list_dic, 'account_type': account_info['account_type'],
                    'show': account_info['show'], 'user_id': user_id}
        else:
            return {'accessToken': access_token, 'refreshToken': refresh_token,
                    'gameList': account_info['game_list'],
                    'channelList': channel_list_dic, 'account_type': account_info['account_type'], 'user_id': user_id}


# cmd ：3
def refresh_user_token(refresh_token):
    """
    刷新token
    :param refresh_token:
    :return:
    """
    ret = verify_token(refresh_token, 'refresh')
    if ret['status']:
        return ret['status']
    user_id = ret['data'].get('user_id')
    token = generate_token(user_id, "access")
    return {'accessToken': token}


