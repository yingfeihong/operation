# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: QL Liu
"""
import re
from base.log.log_manager import LogManager as Log
from base.db.db_manager import DBManager
import datetime
from bson import ObjectId
from app.constant.admin import APP_STORE, CHANNEL_MAP_DB
from share import action_status_code as code


# cmd ：4
def index_pay(data):
    Log.logger.info('data:%s' % data)
    if data:
        if data['gameName'] == u'马赛克英雄':
            del data['gameName']
            result_list = []
            in_list = []
            data2 = {}
            default = 0
            for key, values in data.items():
                in_list.append((key, values))
            for da_ta in in_list:
                if da_ta[0] == u'purchase_time':
                    data2[da_ta[0]] = {"$gte": da_ta[1][0], "$lte": da_ta[1][1]}
                elif da_ta[0] == 'channel_type':
                    default = 1
                    data2['channel_type'] = da_ta[1]
                elif da_ta[0] == 'role_name':
                    if data['channel_type'] == APP_STORE:
                        role = DBManager.get_record('role_data', 'iosgame',
                                                    {'role_name': da_ta[1]})
                    else:
                        role = DBManager.get_record('role_data', 'androidgame',
                                                    {'role_name': da_ta[1]})
                    del data2['channel_type']
                    if role:
                        data2['role_id'] = str(role['_id'])
                    else:
                        return code.USER_NOT_EXIST
                else:
                    data2[da_ta[0]] = da_ta[1]
            if default == 0 or data['channel_type'] == APP_STORE:
                cashes = DBManager.get_multi_record('cash_purchase_order', 'iosgame', data2,)
                for cash in cashes:
                    # 找不到玩家的订单异常捕获
                    try:
                        role_name = DBManager.get_record('role_data', 'iosgame',
                                                         {'_id': ObjectId(cash['role_id'])})['role_name']
                        deliver_time = cash.get('deliver_time') if cash.get('deliver_time') and cash['status'] == 2 \
                            else 0
                        result = {'transaction_id': cash['transaction_id'],
                                  'game': '马赛克英雄', 'channel_type': cash['channel_type'], 'price': cash['price'],
                                  'purchase_time': cash['purchase_time'], 'status': cash['status'],
                                  'deliver_time': deliver_time, 'role_name': role_name}
                        result_list.append(result)
                    except Exception as e:
                        Log.logger.info('订单错误{}'.format(e))
            else:
                cashes = DBManager.get_multi_record('cash_purchase_order', 'androidgame', data2)
                for cash in cashes:
                    try:
                        role_name = DBManager.get_record('role_data', 'androidgame',
                                                         {'_id': ObjectId(cash['role_id'])})['role_name']
                        deliver_time = cash.get('deliver_time') if cash.get('deliver_time') and cash['status'] == 2 \
                            else 0
                        result = {'transaction_id': cash['transaction_id'],
                                  'game': '马赛克英雄', 'channel_type': cash['channel_type'], 'price': cash['price'],
                                  'purchase_time': cash['purchase_time'], 'status': cash['status'],
                                  'deliver_time': deliver_time, 'role_name': role_name}
                        result_list.append(result)
                    except Exception as e:
                        Log.logger.info('订单错误: error:{}'.format(e))

        else:
            result_list = []
            in_list = []
            for key, values in data.items():
                in_list.append((key, values))
            data2 = {}
            Log.logger.warning('in_list:%s' % in_list)
            for da_ta in in_list:
                if da_ta[0] == 'gmtCreate':
                    data2[da_ta[0]] = {"$gte": da_ta[1][0], "$lte": da_ta[1][1]}
                elif da_ta[0] == 'gmtFinish':
                    data2[da_ta[0]] = {'$gte': da_ta[1][0], '$lte': da_ta[1][1]}
                elif da_ta[0] == 'channelName':
                    data2[da_ta[0]] = re.compile(da_ta[1])
                else:
                    data2[da_ta[0]] = da_ta[1]

            orders_info = DBManager.get_multi_record('admin_data_pay', 'admindb', data2)
            for order in orders_info:
                del order['_id']
                result_list.append(order)
    else:
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        seven_day_ago = datetime.datetime.now() - datetime.timedelta(days=3)
        seven_day_ago1 = seven_day_ago.strftime("%Y-%m-%d %H:%M:%S")
        data = {'gmtCreate': {"$lte": now_time, '$gte': seven_day_ago1}}
        Log.logger.warning('data:%s' % data)
        orders_info_1 = DBManager.get_multi_record('admin_data_pay', 'admindb', data)
        result_list = []
        for order in orders_info_1:
            del order['_id']
            result_list.append(order)
    return {'data': result_list}

