# -*- coding:utf-8 -*-

from base.db.db_manager import DBManager
from share import action_status_code as code
from base.encrypt.encrypt import encrypt_md5


# cmd 10
def create_account(data):
    """
    管理员操作
    :param data:
    :return:
    """
    # 删除用户
    if data['type'] == 0:
        account = DBManager.get_record('admin_account', 'admindb', {'account': data['account']})
        if account:
            DBManager.delete_record('admin_account', 'admindb', {'account': data['account']})
            return code.DELETE_SUCCESS
        else:
            return code.USER_NOT_EXIST
    # 创建用户
    elif data['type'] == 1:
        account = DBManager.get_record('admin_account', 'admindb', {'account': data['account']})
        if account:
            return code.THE_ACCOUNT_EXIST
        elif not check_password(data['password']):
            return code.FAIL
        else:
            result = {
                'account_type': data['account_type'],
                'account': data['account'],
                'password': encrypt_md5(str(data['password'])),
                'game_list': data['game_list'],
                'channel_list': data['channel_list'],
                'show': data['show']
            }
            DBManager.insert_record('admin_account', 'admindb', result)
            return code.CREATE_SUCCESS
    # 修改用户
    elif data['type'] == 2:
        account = DBManager.get_record('admin_account', 'admindb', {'account': data['account']})
        if account:
            result = {
                'account_type': data['account_type'],
                'account': data['account'],
                'password': encrypt_md5(str(data['password'])),
                'game_list': data['game_list'],
                'channel_list': data['channel_list'],
                'show': data['show']
            }
            DBManager.update_one('admin_account', 'admindb', {'account': account['account']}, result)
            return code.UPDATA_SUCCESS
        else:
            return code.USER_NOT_EXIST
    # 渠道管理
    else:
        company = data['company']
        channel_name = data['channel_name']
        channel = DBManager.get_record('channel_all', 'admindb', {'big_channel': company})
        if not channel:
            return code.USER_NOT_EXIST
        channel_list = channel['channel_list']
        if channel_name in channel_list:
            return code.THE_ACCOUNT_EXIST
        channel_list.append(channel_name)
        DBManager.update_property('channel_all', 'admindb', {'big_channel': company}, 'channel_list', channel_list)
        return code.OK


def check_password(password):
    word_list = ['!', '@', '#', '$', '%', '^', '&', '*', '~']
    if len(password) < 7 or len(password) > 15:
        return False
    counter = 0
    for i in password:
        if i in word_list:
            counter += 1
    if counter < 1:
        return False
    return True



