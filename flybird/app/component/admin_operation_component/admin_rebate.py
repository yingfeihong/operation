# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: QL Liu
"""

from base.db.db_manager import DBManager
from base.encrypt.encrypt import encrypt_md5
from app.constant.admin import PAYMENT_STATUS
from app.component.admin_operation_component.limited_author import limited_author
from share import action_status_code as code


# cmd ：9
def rebate(data):
    author = limited_author(data['user_id'])
    if not author:
        return code.AUTHOR_NOT
    del data['user_id']
    #  传数据
    result_1 = {}
    result_2 = {}
    account = data['account']
    password = data['password']
    account1 = DBManager.get_record('t_account_info', 'game2', {'account': account})
    account2 = DBManager.get_record('t1_account_info', 'game3', {'account': account})
    if not account1 and not account2:
        return {'data': {'msg': '账户不存在'}}

    if account1:
        if encrypt_md5(password) == account1['password']:
            role = DBManager.get_record('t_role_data','game2',{'user_id':str(account1['_id'])})
            if role:
                res_list = []
                spe = 0
                res = DBManager.get_multi_record('t_cash_purchase_order', 'game2',
                                                 {'role_id': str(role['_id']), 'status': PAYMENT_STATUS.SUCCESS})
                for pay in res:
                    res_list.append(pay['price'])
                    if pay['price'] == 98 and pay['product_id'] in [11, 12, 13]:
                        spe += 1
                result_1['price'] = sum(res_list)
                result_1['spe'] = spe
            else:
                result_1['msg'] = '未注册该角色'
        else:
            result_1['msg'] = '密码错误'
    else:
        result_1['msg'] = '三月账户不存在'

    if account2:
        if encrypt_md5(password) == account2['password']:
            role2 = DBManager.get_record('t1_role_data', 'game3', {'user_id': str(account2['_id'])})
            if role2:
                res_list = []
                spe = 0
                res = DBManager.get_multi_record('t1_cash_purchase_order', 'game3',
                                                 {'role_id': str(role2['_id']), 'status': PAYMENT_STATUS.SUCCESS})
                for pay in res:
                    res_list.append(pay['price'])
                    if pay['price'] == 98 and pay['product_id'] in [11, 12, 13]:
                        spe += 1
                result_2['price'] = sum(res_list)
                result_2['spe'] = spe
            else:
                result_2['msg'] = '未注册该角色'
        else:
            result_2['msg'] = '密码错误'
    else:
        result_2['msg'] = '六月账户不存在'

    return {'data': [result_1, result_2]}
