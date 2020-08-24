# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: QL Liu
"""

from base.log.log_manager import LogManager as Log
from base.db.db_manager import DBManager
import datetime
import re
from app.constant.admin import APP_STORE


# cmd ：7
def index_ltv(data):
    #  传参展示数据
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
                if da_ta[0] == 'date':
                    data2[da_ta[0]] = {"$gte": da_ta[1][0], "$lte": da_ta[1][1]}
                elif da_ta[0] == 'channelName':
                    default = 1
                    data2['channelName'] = da_ta[1]
                else:
                    data2[da_ta[0]] = da_ta[1]
            if default == 0 or data['channelName'] == APP_STORE:
                print 888888
                print data2
                ltvs = DBManager.get_multi_record('ltv_counter', 'admindb', data2)
            else:
                ltvs = DBManager.get_multi_record('ltv_counter_android', 'admindb', data2)
            for ltv in ltvs:
                del ltv['_id']
                result_list.append(ltv)
        else:
            in_list = []
            for key, values in data.items():
                in_list.append((key, values))
            data2 = {}
            Log.logger.warning('in_list:%s' % in_list)
            for da_ta in in_list:
                if da_ta[0] == 'date':
                    # 如果传了起始和结束时间
                    data2[da_ta[0]] = {"$gte": da_ta[1][0], "$lte": da_ta[1][1]}
                elif da_ta[0] == 'channelName':
                    data2[da_ta[0]] = re.compile(da_ta[1])
                else:
                    data2[da_ta[0]] = da_ta[1]
            Log.logger.warning('data2:%s' % data2)
            orders_info = DBManager.get_multi_record('admin_data_ltv', 'admindb', data2)
            result_list = []
            for order in orders_info:
                del order['_id']
                result_list.append(order)
    #  默认数据
    else:
        Log.logger.warning('data none')
        now_time = datetime.datetime.now()
        thirty_day_ago = datetime.datetime.now() - datetime.timedelta(days=30)
        data = {'date': {"$lte": now_time.strftime("%Y-%m-%d"), '$gte': thirty_day_ago.strftime("%Y-%m-%d")}}
        orders_info = DBManager.get_multi_record('admin_data_ltv', 'admindb', data)
        result_list = []
        for order in orders_info:
            del order['_id']
            result_list.append(order)

    return {'data': result_list}
