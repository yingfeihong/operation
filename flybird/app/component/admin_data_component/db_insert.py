# -*- coding:utf-8 -*-
from __future__ import division
import time
import json
import datetime
import requests
from bson import ObjectId
from base.db.db_manager import DBManager
from base.log.log_manager import LogManager as Log
from tool.time_change import timestamp_to_time,time_to_timestamp,time_add,time_add_detail
from app.constant.admin import CHANNEL_LIST


# 马赛克日数据
def all_insert():
    # 第一步：拿到全部账户数据对象 all_account
    now = datetime.datetime.now()
    now_time = now.strftime("%Y-%m-%d")  # 获取当天时间
    all_account = DBManager.get_multi_record('account_info', 'iosgame')
    # 第二步：拿到所有账户渠道列表,日期
    list_channel_all = []
    date_list = []
    for element in all_account:
        list_channel_all.append(element['channel_type'])
        date_list.append(timestamp_to_time(element['register_time']))
    # 数据去重
    list_channel = list(set(list_channel_all))
    date_list = list(set(date_list))
    # 遍历所有渠道所有日期
    for date in date_list:
        print 'start'
        print time_add(date, -1)
        print time_add(date, -2)
        print time_add(date, -3)
        print time_add(date, -4)
        one_date = time_to_timestamp(date)
        for channel_object in list_channel:
            # 新增用户
            new_user = 0
            # 新增角色
            new_role = 0
            # 新增付费人数
            new_increase_pay = 0
            # 新增付费额度
            new_increase_limit = 0
            # 付费总额
            all_pay = 0
            for element in DBManager.get_multi_record('account_info', 'iosgame',
                                                      {'register_time': {'$lte': one_date+43200,
                                                                         '$gte': one_date-43200},
                                                       'channel_type': channel_object}):
                new_user += 1
                role = DBManager.get_record('role_data', 'iosgame', {'user_id': str(element['_id'])})
                if role:
                    new_role += 1
                    if DBManager.get_record('cash_purchase_order', 'iosgame', {'role_id': str(role['_id']),
                                                                               'status': 2, 'purchase_time':
                                                                                   {'$lte': one_date+43200,
                                                                                    '$gte': one_date-43200},
                                                                               'channel_type': channel_object}):
                        new_increase_pay += 1
                    # android需要注意
                    cashs = DBManager.get_multi_record('cash_purchase_order', 'iosgame',
                                                       {'role_id': str(role['_id']), 'status': 2, 'purchase_time':
                                                           {'$lte': one_date+43200, '$gte': one_date-43200},
                                                        'channel_type': channel_object})
                    for cash in cashs:
                        new_increase_limit += cash['price']

            # 付费总人数
            all_pay_account = []
            all_account = DBManager.get_multi_record('cash_purchase_order',
                                                     'iosgame', {'channel_type': channel_object, 'status': 2,
                                                                 'purchase_time': {'$lte': one_date+43200,
                                                                                   '$gte': one_date-43200}})
            for i in all_account:
                if DBManager.get_record('role_data', 'iosgame', {'_id': ObjectId(i['role_id'])}):
                    all_pay_account.append(ObjectId(i['role_id']))
            all_pay_account = len(set(all_pay_account))
            # 付费总额
            all_cashs = DBManager.get_multi_record('cash_purchase_order', 'iosgame',
                                                   {'channel_type': channel_object, 'status': 2,
                                                    'purchase_time': {'$lte': one_date+43200, '$gte': one_date-43200}})
            for cash in all_cashs:
                # 当日所有订单
                all_pay += cash['price']
            if all_pay_account != 0:
                # ARPPU：付费金额/付费账户数
                arppu = all_pay/all_pay_account
            else:
                arppu = '--'
            # 老用户付费人数
            old_pay_account = all_pay_account - new_increase_pay
            # 老用户付费总额
            old_pay_account_limit = all_pay - new_increase_limit
            result = {
                'date': date,
                'channel_type': channel_object,
                'new_user': new_user,
                'new_role': new_role,
                'new_increase_pay': new_increase_pay,
                'new_increase_limit': new_increase_limit,
                'all_pay_account': all_pay_account,
                'all_pay': all_pay,
                'arppu': arppu,
                'old_pay_account': old_pay_account,
                'old_pay_account_limit': old_pay_account_limit,
                'one_leave': 0,
                'three_leave': 0,
                'four_leave': 0,
                'seven_leave': 0,
                'fourteen_leave': 0,
                'thirty_leave': 0,
                'sixty_leave': 0
            }

            if DBManager.get_record('ios_day_data', 'admindb', {'date': date, 'channel_type': channel_object}):
                DBManager.update_one('ios_day_data', 'admindb', {'date': date, 'channel_type': channel_object}, result)
                Log.logger.info('日数据更新')
            else:
                DBManager.insert_record('ios_day_data', 'admindb', result)
                Log.logger.info('日数据插入')


# 马赛克ltv数据
def msk_ltv():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    # 先获取渠道列表
    channel_list = []
    date_list = []
    accounts = DBManager.get_multi_record('account_info', 'iosgame')
    for account in accounts:
        channel_list.append(account['channel_type'])
        register_time = timestamp_to_time(account['register_time'])
        date_list.append(register_time)
    channel_list = list(set(channel_list))
    date_list = list(set(date_list))
    print date_list
    for date in date_list:
        one_date = time_to_timestamp(date)
        for channel in channel_list:
            print date
            print now_time
            d1 = datetime.datetime.strptime(now_time, '%Y-%m-%d')
            d2 = datetime.datetime.strptime(date, '%Y-%m-%d')
            delta = (d1 - d2).days
            account = 0
            account_list = []
            accounts = DBManager.get_multi_record('account_info', 'iosgame',
                                                  {'channel_type': channel, 'register_time':
                                                      {'$lte': one_date+43200, '$gte': one_date-43200}})
            # 获得当天新增总人数和人数列表
            for act in accounts:
                account += 1
                role = DBManager.get_record('role_data', 'iosgame', {'user_id': str(act['_id'])})
                if role:
                    account_list.append(str(role['_id']))
            price = 0
            for i in range(1,delta+1):
                ltv = 'ltv%s' % i
                date_ltv = time_add(date, i)
                cashs = DBManager.get_multi_record('cash_purchase_order', 'iosgame',
                                                   {'channel_type': channel, 'status': 2, 'purchase_time':
                                                       {'$lte': time_to_timestamp(date_ltv)+43200,
                                                        '$gte': time_to_timestamp(date_ltv)-43200}})
                for cash in cashs:
                    if cash['role_id'] in account_list:
                        price += cash['price']
                print 'price:%d' % price
                if DBManager.get_record('ios_data_ltv', 'admindb', {'channelName': channel, 'date': date}):
                    if account != 0:
                        DBManager.update_property('ios_data_ltv', 'admindb',
                                                  {'channelName': channel, 'gameName': '马赛克英雄',
                                                   'date': date}, ltv, price/account)
                        Log.logger.info('LTV数据更新')

                else:
                    print account
                    if account != 0:
                        DBManager.insert_record('ios_data_ltv', 'admindb', {'channelName': channel,
                                                                            'gameName': '马赛克英雄',
                                                                            ltv: price/account, 'date': date})
                        Log.logger.info('LTV数据插入')


# 马赛克时数据
def msk_time_data():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    time_stamp = time_to_timestamp(now_time)
    # 当日新增付费人数
    for i in range(1, 25):
        new_user = DBManager.get_multi_record_count('account_info', 'iosgame',
                                                    {'register_time': {'$gte': time_stamp+(i-1)*3600,
                                                                       '$lte': time_stamp+i*3600}})
        new_role = 0
        new_increase_pay = []
        all_pay_account = []
        new_increase_limit = 0
        all_pay = 0
        for account in DBManager.get_multi_record('account_info', 'iosgame',
                                                  {'register_time': {'$gte': time_stamp+(i-1)*3600,
                                                                     '$lte': time_stamp+i*3600}}):
            role = DBManager.get_record('role_data', 'iosgame', {'user_id': str(account['_id'])})
            if role:
                new_role += 1
                cashs = DBManager.get_multi_record('cash_purchase_order',
                                                   'iosgame', {'role_id': str(role['_id']),
                                                               'status': 2, 'purchase_time':
                                                                            {'$gte': time_stamp+(i-1)*3600,
                                                                             '$lte': time_stamp+i*3600}})
                for cash in cashs:
                    new_increase_pay.append(cash['role_id'])
                    new_increase_limit += cash['price']

        for cash in DBManager.get_multi_record('cash_purchase_order', 'iosgame',
                                               {'status': 2, 'purchase_time': {'$gte': time_stamp+(i-1)*3600,
                                                                               '$lte': time_stamp+i*3600}}):
            all_pay_account.append(cash['role_id'])
            all_pay += cash['price']

        dau = DBManager.get_multi_record_count('role_data', 'iosgame', {'login_time': {'$gte': time_stamp+(i-1)*3600,
                                                                                       '$lte': time_stamp+i*3600}})
        if dau != 0:
            pay_rate = len(set(all_pay_account))/dau
            arpu = all_pay/dau
        else:
            pay_rate = '--'
            arpu = '--'
        if len(set(all_pay_account)) != 0:
            arppu = all_pay/len(set(all_pay_account))
        else:
            arppu = '--'
        time_t = 'time%d' % i
        result = {
            'date': now_time,
            'channel_type': 'appstore',
            'time': time_t,
            'new_user': new_user,
            'new_role': new_role,
            'new_increase_pay': len(set(new_increase_pay)),
            'all_pay_account': len(set(all_pay_account)),
            'new_increase_limit': new_increase_limit,
            'all_pay': all_pay,
            'dau': dau,
            'pay_rate': pay_rate,
            'arpu': arpu,
            'arppu': arppu,
        }
        if DBManager.get_record('ios_time', 'admindb', {'date': now_time, 'time': time_t}):
            DBManager.update_one('ios_time', 'admindb', {'date': now_time, 'time': time_t},result)
            Log.logger.info('时数据更新')
        else:
            DBManager.insert_record('ios_time', 'admindb', result)
            Log.logger.info('时数据插入')


# 马赛克ios留存和dau数据
def day_insert():
    # 第一步：拿到全部账户数据对象 all_account
    now = datetime.datetime.now()
    now_time = now.strftime("%Y-%m-%d")  # 获取当天时间
    time_stamp = time.time()
    # 当天新增用户
    new_role = 0
    new_increase_pay = []
    new_increase_limit = 0
    all_pay_account = []
    all_pay = 0
    new_user = DBManager.get_multi_record_count('account_info', 'iosgame',
                                                {'register_time': {'$gte': time_stamp-24*3600}})
    for account in DBManager.get_multi_record('account_info', 'iosgame',
                                              {'register_time': {'$gte': time_stamp-24*3600}}):
        role = DBManager.get_record('role_data', 'iosgame',
                                    {'login_time': {'$gte': time_stamp-24*3600}, 'user_id': str(account['_id'])})
        if role:
            new_role += 1
            for cash in DBManager.get_multi_record('cash_purchase_order', 'iosgame',
                                                   {'role_id': str(role['_id']), 'status': 2,
                                                    'purchase_time': {'$gte': time_stamp-24*3600}}):
                new_increase_pay.append(cash['role_id'])
                new_increase_limit += cash['price']
    for cash in DBManager.get_multi_record('cash_purchase_order', 'iosgame',
                                           {'purchase_time': {'$gte': time_stamp - 24*3600}, 'status': 2}):
        all_pay_account.append(cash['role_id'])
        all_pay += cash['price']
    dau = DBManager.get_multi_record_count('role_data', 'iosgame', {'login_time': {'$gte': time_stamp-24*3600}})
    for role in DBManager.get_multi_record('role_data', 'iosgame', {'login_time': {'$gte': time_stamp-24*3600}}):
        account = DBManager.get_record('account_info', 'iosgame', {'_id': ObjectId(role['user_id'])})
        if time_stamp-24*3600-86400 < account['register_time'] < time_stamp-24*3600:
            one_date = time_add(now_time, -1)
            DBManager.inc_property('ios_day_data', 'admindb', {'date': one_date}, 'one_leave', 1)
            Log.logger.info('留存数据更新')
        elif time_stamp-24*3600-2*86400 < account['register_time'] < time_stamp-24*3600-1*86400:
            three_date = time_add(now_time, -2)
            DBManager.inc_property('ios_day_data', 'admindb', {'date': three_date}, 'three_leave', 1)
            Log.logger.info('留存数据更新')
        elif time_stamp-24*3600-3*86400 < account['register_time'] < time_stamp-24*3600-2*86400:
            four_date = time_add(now_time, -3)
            DBManager.inc_property('ios_day_data', 'admindb', {'date': four_date}, 'four_leave', 1)
            Log.logger.info('留存数据更新')
        elif time_stamp-24*3600-6*86400 < account['register_time'] < time_stamp-24*3600-5*86400:
            seven_date = time_add(now_time, -6)
            DBManager.inc_property('ios_day_data', 'admindb', {'date': seven_date}, 'seven_leave', 1)
            Log.logger.info('留存数据更新')
        elif time_stamp - 24*3600 - 13*86400 < account['register_time'] < time_stamp - 24*3600 - 12*86400:
            fourteen_date = time_add(now_time, -13)
            DBManager.inc_property('ios_day_data', 'admindb', {'date': fourteen_date}, 'fourteen_leave', 1)
            Log.logger.info('留存数据更新')
        elif time_stamp - 24*3600 - 29*86400 < account['register_time'] < time_stamp - 24*3600 - 28*86400:
            thirty_date = time_add(now_time, -29)
            DBManager.inc_property('ios_day_data', 'admindb', {'date': thirty_date}, 'thirty_leave', 1)
            Log.logger.info('留存数据更新')
        elif time_stamp - 24*3600 - 59*86400 < account['register_time'] < time_stamp - 24*3600 - 58*86400:
            sixty_date = time_add(now_time, -59)
            DBManager.inc_property('ios_day_data', 'admindb', {'date': sixty_date}, 'sixty_leave', 1)
            Log.logger.info('留存数据更新')
        else:
            Log.logger.info('留存数据未更新')
    new_increase_pay = len(set(new_increase_pay))
    all_pay_account = len(set(all_pay_account))
    if dau != 0:
        pay_rate = all_pay_account/dau
        arpu = all_pay/dau
    else:
        pay_rate = '--'
        arpu = '--'
    if all_pay_account != 0:
        arppu = all_pay/all_pay_account
    else:
        arppu = '--'
    old_pay_account = all_pay_account - new_increase_pay
    old_pay_account_limit = all_pay - new_increase_limit
    result = {
                'date': now_time,
                'game': '马赛克英雄',
                'channel_type': 'appstore',
                'new_user': new_user,
                'new_role': new_role,
                'new_increase_pay': new_increase_pay,
                'new_increase_limit': new_increase_limit,
                'all_pay_account': all_pay_account,
                'all_pay': all_pay,
                'arppu': arppu,
                'pay_rate': pay_rate,
                'arpu': arpu,
                'dau': dau,
                'old_pay_account': old_pay_account,
                'old_pay_account_limit': old_pay_account_limit,
                'one_leave': 0,
                'three_leave': 0,
                'four_leave': 0,
                'seven_leave': 0,
                'fourteen_leave': 0,
                'thirty_leave': 0,
                'sixty_leave': 0
            }

    if DBManager.get_record('ios_day_data', 'admindb', {'date': now_time, 'channel_type': 'appstore'}):
        DBManager.update_one('ios_day_data', 'admindb', {'date': now_time, 'channel_type': 'appstore'}, result)
        Log.logger.info('日数据更新')
    else:
        DBManager.insert_record('ios_day_data', 'admindb', result)
        Log.logger.info('日数据插入')


# 传奇账单数据
def cq_pay():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    url = 'https://m.lianhuigame.com/pay/queryOrder.json'
    data = {'startDate': '2019-01-01 16:13:00', 'endDate': now_time, 'type': 1}
    result = json.loads(requests.post(url, data=data).text)
    for data in result['result']:
        # 如果订单id不存在，则插入
        if DBManager.get_record('admin_data_pay', 'admindb', {'orderNo': data['orderNo']}):
            Log.logger.info('订单存在')
            DBManager.update_one('admin_data_pay', 'admindb', {'orderNo': data['orderNo']}, data)
        else:
            DBManager.insert_record('admin_data_pay', 'admindb', data)
            Log.logger.info('订单插入')


# 传奇账户流水数据插入
def cq_account():
    url = 'https://m.lianhuigame.com//user/queryUser.json'
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_time = time_add_detail(now_time, -1)
    data = {'startDate': start_time, 'endDate': now_time}
    result = json.loads(requests.post(url, data=data).text)
    for data in result['result']:
        # 如果账户id不存在，则插入
        if DBManager.get_record('admin_account_data', 'admindb', {'userId': data['userId']}):
            Log.logger.info(' 账户存在')
        else:
            DBManager.insert_record('admin_account_data', 'admindb', data)
            Log.logger.info('账户插入插入')


# 传奇日数据
def cq_day():
    # 先获取渠道列表
    channel_list = []
    game_list = []
    date_list = []
    accounts = DBManager.get_multi_record('admin_account_data', 'admindb')
    cashes = DBManager.get_multi_record('admin_data_pay', 'admindb')
    for account in accounts:
        channel_list.append(account['channelName'])
        game_list.append(account['gameName'])
        date_list.append(account['gmtCreate'])
        for cash in cashes:
            channel_list.append(cash['channelName'])
            game_list.append(cash['gameName'])
            date_list.append(cash['gmtCreate'].split(' ')[0])
    channel_list = list(set(channel_list))
    game_list = list(set(game_list))
    date_list = list(set(date_list))
    print channel_list
    print game_list
    print date_list
    for date in date_list:
        for game in game_list:
            for channel in channel_list:
                new_user = 0
                new_role = 0
                new_increase_pay = []
                new_increase_limit = 0
                all_pay_account = []
                all_pay = 0
                for user in DBManager.get_multi_record('admin_account_data', 'admindb',
                                                       {'channelName': channel, 'gameName': game, 'gmtCreate': date}):
                    new_user += 1
                    new_role += 1
                    cash1 = DBManager.get_record('admin_data_pay', 'admindb',
                                                 {'userId': user['userId'], 'channelName': channel,
                                                  'gameName': game, 'status': 'success'})
                    if cash1:
                        if cash1['gmtCreate'].split(' ')[0] == date:
                            new_increase_pay.append(cash1['userId'])
                            new_increase_limit += int(cash1['amount'].split('.')[0].replace(',',''))
                pays = DBManager.get_multi_record('admin_data_pay', 'admindb',
                                                  {'channelName': channel, 'gameName': game, 'status': 'success'})
                for pay in pays:
                    if pay['gmtCreate'].split(' ')[0] == date:
                        all_pay_account.append(pay['userId'])
                        all_pay += int(pay['amount'].split('.')[0].replace(',', ''))
                all_pay_account = len(set(all_pay_account))
                new_increase_pay = len(set(new_increase_pay))
                if all_pay_account != 0:
                    arppu = all_pay/all_pay_account
                else:
                    arppu = '--'
                old_pay_account = all_pay_account - new_increase_pay
                old_pay_account_limit = all_pay - new_increase_limit
                result = {
                    'date': date,
                    'channel_type': channel,
                    'new_user': new_user,
                    'new_role': new_role,
                    'new_increase_pay': new_increase_pay,
                    'new_increase_limit': new_increase_limit,
                    'all_pay_account': all_pay_account,
                    'all_pay': all_pay,
                    'arppu': arppu,
                    'old_pay_account': old_pay_account,
                    'old_pay_account_limit': old_pay_account_limit,
                    'gameName': game
                }
                if DBManager.get_record('admin_day_data', 'admindb',
                                        {'date': date, 'channel_type': channel, 'gameName': game}):
                    DBManager.update_one('admin_day_data', 'admindb',
                                         {'date': date, 'channel_type': channel, 'gameName': game}, result)
                    Log.logger.info('日数据更新')
                else:
                    DBManager.insert_record('admin_day_data', 'admindb', result)
                    Log.logger.info('日数据插入')


# 传奇ltv数据
def cq_ltv():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    # 先获取渠道列表
    channel_list = []
    game_list = []
    date_list = []
    accounts = DBManager.get_multi_record('admin_account_data', 'admindb')
    cashes = DBManager.get_multi_record('admin_data_pay', 'admindb')
    for account in accounts:
        channel_list.append(account['channelName'])
        game_list.append(account['gameName'])
        date_list.append(account['gmtCreate'])
        for cash in cashes:
            channel_list.append(cash['channelName'])
            game_list.append(cash['gameName'])
            date_list.append(cash['gmtCreate'].split(' ')[0])
    channel_list = list(set(channel_list))
    game_list = list(set(game_list))
    date_list = list(set(date_list))
    print date_list
    print channel_list
    print game_list
    for date in date_list:
        for game in game_list:
            for channel in channel_list:
                # 获得当天新增总人数和人数列表
                accounts = DBManager.get_multi_record_count('admin_account_data', 'admindb',
                                                            {'channelName': channel,
                                                             'gameName': game, 'gmtCreate': date})
                account_id = []
                for account in DBManager.get_multi_record('admin_account_data', 'admindb',
                                                          {'channelName': channel,
                                                           'gameName': game, 'gmtCreate': date}):
                    account_id.append(account['userId'])
                all_cash = 0
                d1 = datetime.datetime.strptime(now_time, '%Y-%m-%d')
                d2 = datetime.datetime.strptime(date, '%Y-%m-%d')
                delta = (d1 - d2).days
                for i in range(1, delta+1):
                    ltv = 'ltv%d'%i
                    day_other = time_add(date, i)
                    cashs = DBManager.get_multi_record('admin_data_pay', 'admindb',
                                                       {'channelName': channel, 'gameName': game, 'status': 'success'})
                    for cash2 in cashs:
                        if cash2['gmtCreate'].split(' ')[0] == day_other:
                            if cash2['userId'] in account_id:
                                all_cash += int(cash2['amount'].split('.')[0].replace(',', ''))
                    if DBManager.get_record('admin_data_ltv', 'admindb',
                                            {'channelName': channel, 'gameName': game, 'date': date}):
                        if accounts != 0:
                            DBManager.update_property('admin_data_ltv', 'admindb',
                                                      {'channelName': channel, 'gameName': game, 'date': date}, ltv,
                                                      all_cash/accounts)
                            Log.logger.info('LTV数据更新')
                    else:
                        if accounts != 0:
                            DBManager.insert_record('admin_data_ltv', 'admindb',
                                                    {'channelName': channel, 'gameName': game,
                                                     ltv: all_cash/accounts, 'date':date})
                            Log.logger.info('LTV数据插入')


# 传奇账户流水时数据插入
def cq_account_time():
    url = 'https://m.lianhuigame.com//user/queryUser.json'
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    now_time = now_time + ' ' + '00:00:00'
    hour_list = [now_time]
    for hour in range(1, 25):
        start_time = time_add_detail(now_time, hour / 24)
        hour_list.append(start_time)
    for index in range(24):
        data = {'startDate': hour_list[index], 'endDate': hour_list[index+1]}
        result = json.loads(requests.post(url, data=data).text)
        for data in result['result']:
            # 如果账户id不存在，则插入
            data['detail_time'] = [hour_list[index], hour_list[index+1]]
            if DBManager.get_record('admin_account_time', 'admindb', {'userId': data['userId']}):
                Log.logger.info(' 账户存在')
            else:
                DBManager.insert_record('admin_account_time', 'admindb', data)
                Log.logger.info('账户插入插入')


# 传奇时数据
def cq_time_data():
    # 先获取渠道列表
    channel_list = []
    game_list = []
    time_list = []
    accounts = DBManager.get_multi_record('admin_account_data', 'admindb')
    cashes = DBManager.get_multi_record('admin_data_pay', 'admindb')
    for account in accounts:
        channel_list.append(account['channelName'])
        game_list.append(account['gameName'])
        for cash in cashes:
            channel_list.append(cash['channelName'])
            game_list.append(cash['gameName'])
        if account['gmtCreate'] not in time_list:
            time_list.append(account['gmtCreate'])
    print time_list
    channel_list = list(set(channel_list))
    game_list = list(set(game_list))
    for hour in time_list:
        for game in game_list:
            for channel in channel_list:
                new_user = 0
                new_role = 0
                new_increase_pay = []
                new_increase_limit = 0
                all_pay_account = []
                all_pay = 0
                for user in DBManager.get_multi_record('admin_account_time', 'admindb',
                                                       {'channelName': channel, 'gameName': game, 'detail_time': hour}):
                    new_user += 1
                    new_role += 1
                    cash1 = DBManager.get_record('admin_data_pay', 'admindb',
                                                 {'userId': user['userId'],
                                                  'channelName': channel, 'gameName': game, 'status': 'success'})
                    if cash1:
                        if hour[0] <= cash1['gmtCreate'] < hour[1]:
                            new_increase_pay.append(cash1['userId'])
                            new_increase_limit += int(cash1['amount'].split('.')[0].replace(',', ''))
                pays = DBManager.get_multi_record('admin_data_pay', 'admindb',
                                                  {'channelName': channel, 'gameName': game, 'status': 'success'})
                for pay in pays:
                    if hour[0] <= pay['gmtCreate'] < hour[1]:
                        all_pay_account.append(pay['userId'])
                        all_pay += int(pay['amount'].split('.')[0].replace(',', ''))
                all_pay_account = len(set(all_pay_account))
                new_increase_pay = len(set(new_increase_pay))
                if all_pay_account != 0:
                    arppu = all_pay/all_pay_account
                else:
                    arppu = '--'
                old_pay_account = all_pay_account - new_increase_pay
                old_pay_account_limit = all_pay - new_increase_limit
                result = {
                    'date': hour[0].split(' ')[0],
                    'hour': hour,
                    'channel_type': channel,
                    'new_user': new_user,
                    'new_role': new_role,
                    'new_increase_pay': new_increase_pay,
                    'new_increase_limit': new_increase_limit,
                    'all_pay_account': all_pay_account,
                    'all_pay': all_pay,
                    'arppu': arppu,
                    'old_pay_account': old_pay_account,
                    'old_pay_account_limit': old_pay_account_limit,
                    'gameName': game
                }
                if DBManager.get_record('admin_time_data', 'admindb',
                                        {'hour': hour, 'channel_type': channel, 'gameName': game}):
                    DBManager.update_one('admin_time_data', 'admindb',
                                         {'hour': hour, 'channel_type': channel, 'gameName': game}, result)
                    Log.logger.info('时数据更新')
                else:
                    DBManager.insert_record('admin_time_data', 'admindb', result)
                    Log.logger.info('时数据插入')


# 马赛克android留存和dau数据
def android_day_insert():
    # 第一步：拿到全部账户数据对象 all_account
    now = datetime.datetime.now()
    now_time = now.strftime("%Y-%m-%d")  # 获取当天时间
    time_stamp = time.time()
    # now = datetime.datetime.now()
    # now_time = now.strftime("%Y-%m-%d")  # 获取当天时间
    # now_time = time_add(now_time, -1)
    # time_stamp = time.time()
    # time_stamp = time_stamp - 24 * 3600
    # 找到所有渠道
    channel_list = CHANNEL_LIST
    for channel in channel_list:
        # 当天新增用户
        new_role = 0
        new_increase_pay = []
        new_increase_limit = 0
        all_pay_account = []
        all_pay = 0
        new_user = DBManager.get_multi_record_count('account_info', 'androidgame',
                                                    {'register_time': {'$gte':time_stamp-24*3600},
                                                     'channel_type_ex': channel})
        for account in DBManager.get_multi_record('account_info', 'androidgame',
                                                  {'register_time': {'$gte': time_stamp-24*3600},
                                                   'channel_type_ex': channel}):
            role = DBManager.get_record('role_data', 'androidgame', {'login_time': {'$gte':time_stamp-24*3600},
                                                                     'user_id': str(account['_id'])})
            if role:
                new_role += 1
                for cash in DBManager.get_multi_record('cash_purchase_order', 'androidgame',
                                                       {'role_id': str(role['_id']), 'status': 2, 'purchase_time':
                                                           {'$gte': time_stamp-24*3600},  'channel_type': channel}):
                    new_increase_pay.append(cash['role_id'])
                    new_increase_limit += cash['price']
        for cash in DBManager.get_multi_record('cash_purchase_order', 'androidgame',
                                               {'purchase_time': {'$gte': time_stamp - 24*3600},
                                                'status': 2,  'channel_type': channel}):
            all_pay_account.append(cash['role_id'])
            all_pay += cash['price']
        dau = 0
        for d in DBManager.get_multi_record('role_data', 'androidgame',
                                            {'login_time': {'$gte': time_stamp-24*3600}}):
            ac = DBManager.get_record('account_info', 'androidgame',
                                      {'_id': ObjectId(str(d['user_id'])), 'channel_type_ex': channel})
            if ac:
                dau += 1
        for role in DBManager.get_multi_record('role_data', 'androidgame',
                                               {'login_time': {'$gte': time_stamp-24*3600}}):
            account = DBManager.get_record('account_info', 'androidgame',
                                           {'_id':ObjectId(role['user_id']), 'channel_type_ex': channel})
            try :
                if time_stamp-24*3600-86400 < account['register_time'] < time_stamp-24*3600:
                    one_date = time_add(now_time, -1)
                    DBManager.inc_property('android_day_data', 'admindb',
                                           {'date': one_date,  'channel_type': channel}, 'one_leave', 1)
                    Log.logger.info('留存数据更新')
                elif time_stamp-24*3600-2*86400 < account['register_time'] < time_stamp-24*3600-1*86400:
                    three_date = time_add(now_time, -2)
                    DBManager.inc_property('android_day_data','admindb',
                                           {'date': three_date, 'channel_type': channel}, 'three_leave',1)
                    Log.logger.info('留存数据更新')
                elif time_stamp-24*3600-3*86400 < account['register_time'] < time_stamp-24*3600-2*86400:
                    four_date = time_add(now_time, -3)
                    DBManager.inc_property('android_day_data', 'admindb',
                                           {'date': four_date, 'channel_type': channel}, 'four_leave',1)
                    Log.logger.info('留存数据更新')
                elif time_stamp-24*3600-6*86400 < account['register_time'] < time_stamp-24*3600-5*86400:
                    seven_date = time_add(now_time, -6)
                    DBManager.inc_property('android_day_data', 'admindb',
                                           {'date': seven_date, 'channel_type': channel}, 'seven_leave', 1)
                    Log.logger.info('留存数据更新')
                elif time_stamp - 24*3600 - 13*86400 < account['register_time'] < time_stamp - 24*3600 - 12*86400:
                    fourteen_date = time_add(now_time, -13)
                    DBManager.inc_property('android_day_data', 'admindb',
                                           {'date': fourteen_date, 'channel_type': channel}, 'fourteen_leave', 1)
                    Log.logger.info('留存数据更新')
                elif time_stamp - 24*3600 - 29*86400 < account['register_time'] < time_stamp - 24*3600 - 28*86400:
                    thirty_date = time_add(now_time, -29)
                    DBManager.inc_property('android_day_data', 'admindb',
                                           {'date': thirty_date, 'channel_type': channel}, 'thirty_leave', 1)
                    Log.logger.info('留存数据更新')
                elif time_stamp - 24*3600 - 59*86400 < account['register_time'] < time_stamp - 24*3600 - 58*86400:
                    sixty_date = time_add(now_time, -59)
                    DBManager.inc_property('android_day_data', 'admindb',
                                           {'date': sixty_date, 'channel_type': channel}, 'sixty_leave', 1)
                    Log.logger.info('留存数据更新')
                else:
                    Log.logger.info('留存数据未更新')
            except Exception as e:
                Log.logger.info('角色id无关联:{}'.format(e))
        new_increase_pay = len(set(new_increase_pay))
        all_pay_account = len(set(all_pay_account))
        if dau != 0:
            pay_rate = all_pay_account/dau
            arpu = all_pay/dau
        else:
            pay_rate = '--'
            arpu = '--'
        if all_pay_account != 0:
            arppu = all_pay/all_pay_account
        else:
            arppu = '--'
        old_pay_account = all_pay_account - new_increase_pay
        old_pay_account_limit = all_pay - new_increase_limit
        result = {
                    'date': now_time,
                    'game': '马赛克英雄',
                    'channel_type': channel,
                    'new_user': new_user,
                    'new_role': new_role,
                    'new_increase_pay': new_increase_pay,
                    'new_increase_limit': new_increase_limit,
                    'all_pay_account': all_pay_account,
                    'all_pay': all_pay,
                    'arppu': arppu,
                    'pay_rate': pay_rate,
                    'arpu': arpu,
                    'dau': dau,
                    'old_pay_account': old_pay_account,
                    'old_pay_account_limit': old_pay_account_limit,
                    'one_leave': 0,
                    'three_leave': 0,
                    'four_leave': 0,
                    'seven_leave': 0,
                    'fourteen_leave': 0,
                    'thirty_leave': 0,
                    'sixty_leave': 0
                }

        if DBManager.get_record('android_day_data', 'admindb', {'date': now_time, 'channel_type': channel}):
            DBManager.update_one('android_day_data', 'admindb',{'date': now_time, 'channel_type': channel}, result)
            Log.logger.info('安卓日数据更新')
        else:
            DBManager.insert_record('android_day_data', 'admindb', result)
            Log.logger.info('安卓日数据插入')


# android马赛克ltv数据
def android_msk_ltv():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    # 先获取渠道列表
    channel_list = CHANNEL_LIST
    date_list = []
    accounts = DBManager.get_multi_record('account_info', 'androidgame')
    for account in accounts:
        register_time = timestamp_to_time(account['register_time'])
        date_list.append(register_time)
    date_list = list(set(date_list))
    for date in date_list:
        one_date = time_to_timestamp(date)
        for channel in channel_list:
            d1 = datetime.datetime.strptime(now_time, '%Y-%m-%d')
            d2 = datetime.datetime.strptime(date, '%Y-%m-%d')
            delta = (d1 - d2).days
            account = 0
            account_list = []
            accounts = DBManager.get_multi_record('account_info', 'androidgame',
                                                  {'register_time': {'$lte': one_date+43200, '$gte': one_date-43200},
                                                   'channel_type_ex': channel})
            # 获得当天新增总人数和人数列表
            for act in accounts:
                account += 1
                role = DBManager.get_record('role_data', 'androidgame', {'user_id': str(act['_id'])})
                if role:
                    account_list.append(str(role['_id']))
            price = 0
            for i in range(1, delta+1):
                ltv = 'ltv%s' % i
                date_ltv = time_add(date, i)
                cashs = DBManager.get_multi_record('cash_purchase_order', 'androidgame',
                                                   {'channel_type': channel, 'status': 2,
                                                    'purchase_time': {'$lte': time_to_timestamp(date_ltv)+43200,
                                                                      '$gte': time_to_timestamp(date_ltv)-43200}})
                for cash in cashs:
                    if cash['role_id'] in account_list:
                        price += cash['price']
                if DBManager.get_record('android_data_ltv', 'admindb', {'channelName': channel, 'date': date}):
                    if account != 0:
                        DBManager.update_property('android_data_ltv', 'admindb', {'channelName': channel,
                                                                                  'gameName': '马赛克英雄',
                                                                                  'date': date}, ltv, price/account)
                        Log.logger.info('LTV数据更新')

                else:
                    if account != 0:
                        DBManager.insert_record('android_data_ltv', 'admindb', {'channelName': channel,
                                                                                'gameName': '马赛克英雄',
                                                                                ltv: price/account, 'date': date})
                        Log.logger.info('LTV数据插入')


# android马赛克时数据
def android_msk_time_data():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    time_stamp = time_to_timestamp(now_time)
    # 找到所有渠道
    channel_list = CHANNEL_LIST
    for channel in channel_list:
        # 当日新增付费人数
        for i in range(1, 25):
            new_user = DBManager.get_multi_record_count('account_info', 'androidgame',
                                                        {'register_time': {'$gte': time_stamp+(i-1)*3600,
                                                                           '$lte': time_stamp+i*3600},
                                                         'channel_type_ex': channel})
            new_role = 0
            new_increase_pay = []
            all_pay_account = []
            new_increase_limit = 0
            all_pay = 0
            for account in DBManager.get_multi_record('account_info', 'androidgame',
                                                      {'register_time': {'$gte': time_stamp+(i-1)*3600,
                                                                         '$lte': time_stamp+i*3600},
                                                       'channel_type_ex': channel}):
                role = DBManager.get_record('role_data', 'androidgame', {'user_id': str(account['_id']),
                                                                         'login_time': {'$gte': time_stamp+(i-1)*3600,
                                                                                        '$lte': time_stamp+i*3600}})
                if role:
                    new_role += 1
                    cashs = DBManager.get_multi_record('cash_purchase_order', 'androidgame',
                                                       {'role_id': str(role['_id']), 'status': 2,
                                                        'purchase_time':
                                                        {'$gte': time_stamp+(i-1)*3600, '$lte': time_stamp+i*3600},
                                                        'channel_type': channel})
                    for cash in cashs:
                        new_increase_pay.append(cash['role_id'])
                        new_increase_limit += cash['price']

            for cash in DBManager.get_multi_record('cash_purchase_order', 'androidgame',
                                                   {'status': 2, 'purchase_time': {'$gte': time_stamp+(i-1)*3600,
                                                                                   '$lte': time_stamp+i*3600},
                                                    'channel_type': channel}):
                all_pay_account.append(cash['role_id'])
                all_pay += cash['price']

            dau = 0
            for d in DBManager.get_multi_record('role_data', 'androidgame',
                                                {'login_time': {'$gte': time_stamp+(i-1)*3600,
                                                                '$lte': time_stamp+i*3600}}):
                ac = DBManager.get_record('account_info', 'androidgame',
                                          {'_id': ObjectId(str(d['user_id'])), 'channel_type_ex': channel})
                if ac:
                    dau += 1
            if dau != 0:
                pay_rate = len(set(all_pay_account))/dau
                arpu = all_pay/dau
            else:
                pay_rate = '--'
                arpu = '--'
            if len(set(all_pay_account)) != 0:
                arppu = all_pay/len(set(all_pay_account))
            else:
                arppu = '--'
            time_t = 'time%d' % i
            result = {
                'date': now_time,
                'channel_type': channel,
                'time': time_t,
                'new_user': new_user,
                'new_role': new_role,
                'new_increase_pay': len(set(new_increase_pay)),
                'all_pay_account': len(set(all_pay_account)),
                'new_increase_limit': new_increase_limit,
                'all_pay': all_pay,
                'dau': dau,
                'pay_rate': pay_rate,
                'arpu': arpu,
                'arppu': arppu,
            }
            if DBManager.get_record('android_time', 'admindb',
                                    {'date': now_time, 'time': time_t, 'channel_type': channel}):
                DBManager.update_one('android_time', 'admindb',
                                     {'date': now_time, 'time': time_t, 'channel_type': channel}, result)
                Log.logger.info('时数据更新')
            else:
                DBManager.insert_record('android_time', 'admindb', result)
                Log.logger.info('时数据插入')


def dau_role():
    from base.db.db_util import DBUtil
    now = time.time()
    roles = DBManager.get_multi_record('role_data', 'iosgame', {'login_time': {'$gte': now - 3600*24}})
    result = []
    for role in roles:
        name = role['role_name']
        date = timestamp_to_time(now)
        lv = role['role_lv']
        result.append({'role_name': name, 'date': date, 'lv': lv,
                       'cumulative_recharge': role['cumulative_recharge'],
                       'rank': role['rank'], 'diamond': role['diamond']})
    db = DBUtil.get_db_instance('admindb')
    db['dau_role_ios'].insert_many(result)
    Log.logger.info('ok')


def ios_ltv_counter():
    # 第一步： 插入当天DAU数据
    DBManager.insert_record('ltv_counter', 'admindb', {'date': timestamp_to_time(time.time()), 'timestamp': time.time(),
                                                       'channelName': 'appstore', 'gameName':
                                                           '马赛克英雄', 'ltv_list': []})
    role_list = []
    for account in DBManager.get_multi_record('account_info', 'iosgame',
                                              {'register_time': {'$gte': time.time()-86400}}):
        role = DBManager.get_record('role_data', 'iosgame', {'user_id': str(account['_id'])})
        if role:
            role_list.append(str(role['_id']))
    i = DBManager.get_record('ltv_counter', 'admindb',
                             {'date': timestamp_to_time(time.time()), 'channelName': 'appstore',
                              'gameName': '马赛克英雄'})
    DBManager.insert_record('ltv_role', 'admindb', {'role_list': role_list, 'counter_number': len(set(role_list)),
                                                    'date': i['date'], 'counter_id': str(i['_id'])})
    # 第二步， 更新DAU数据
    for record in DBManager.get_multi_record('ltv_counter', 'admindb'):
        obj = DBManager.get_record('ltv_role', 'admindb', {'counter_id': str(record['_id'])})
        role_list = obj['role_list']
        counter_number = obj['counter_number']
        cash_price = 0
        ltv_list = record['ltv_list']
        for cash in DBManager.get_multi_record('cash_purchase_order', 'iosgame',
                                               {'status': 2, 'purchase_time': {'$gte': time.time()-86400},
                                                'role_id': {'$in': role_list}}):
            cash_price += cash['price']
        if ltv_list:
            if counter_number != 0:
                new_ltv = ltv_list[-1] + cash_price/float(counter_number)
                ltv_list.append(new_ltv)
        else:
            if counter_number != 0:
                new_ltv = cash_price/float(counter_number)
                ltv_list.append(new_ltv)
        DBManager.update_one('ltv_counter', 'admindb', {'_id': record['_id']}, {'ltv_list': ltv_list})


def android_ltv_counter():
    # 第一步： 插入当天DAU数据
    date = timestamp_to_time(time.time())
    for channel in CHANNEL_LIST:
        DBManager.insert_record('ltv_counter_android', 'admindb', {'date': date,
                                                                   'timestamp': time.time(), 'channelName': channel,
                                                                   'gameName': '马赛克英雄', 'ltv_list': []})
        role_list = []
        for account in DBManager.get_multi_record('account_info', 'androidgame',
                                                  {'register_time': {'$gte': time.time()-86400},
                                                   'channel_type_ex': channel}):
            role = DBManager.get_record('role_data', 'androidgame', {'user_id': str(account['_id'])})
            if role:
                role_list.append(str(role['_id']))
        i = DBManager.get_record('ltv_counter_android', 'admindb',
                                 {'date': date, 'channelName': channel,
                                  'gameName': '马赛克英雄'})
        DBManager.insert_record('ltv_role_android', 'admindb', {'role_list': role_list,
                                                                'counter_number': len(set(role_list)),
                                                                'date': i['date'], 'counter_id': str(i['_id'])})
    # 第二步， 更新DAU数据
    for record in DBManager.get_multi_record('ltv_counter_android', 'admindb'):
        obj = DBManager.get_record('ltv_role_android', 'admindb', {'counter_id': str(record['_id'])})
        role_list = obj['role_list']
        counter_number = obj['counter_number']
        cash_price = 0
        ltv_list = record['ltv_list']
        for cash in DBManager.get_multi_record('cash_purchase_order', 'androidgame',
                                               {'status': 2, 'purchase_time': {'$gte': time.time()-86400},
                                                'role_id': {'$in': role_list}}):
            cash_price += cash['price']
        if ltv_list:
            if counter_number != 0:
                new_ltv = ltv_list[-1] + cash_price/float(counter_number)
                ltv_list.append(new_ltv)
        else:
            if counter_number != 0:
                new_ltv = cash_price/float(counter_number)
                ltv_list.append(new_ltv)
        DBManager.update_one('ltv_counter_android', 'admindb', {'_id': record['_id']}, {'ltv_list': ltv_list})
