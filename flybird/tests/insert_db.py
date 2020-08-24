# -*- coding:utf-8 -*-

import pymongo
import requests
import json
from bson import ObjectId
from tool.time_change import timestamp_to_time, time_to_timestamp, time_add, time_add_detail
import time
time_list = [1567094400 + i*86400 for i in range(80)]
# client = pymongo.MongoClient("mongodb://yfh:123456@192.168.200.144:27017/")
db = pymongo.MongoClient("s-bp12fefdcdc7d3f4-pub.mongodb.rds.aliyuncs.com:3717")
mycol = db["game"]
mycol.authenticate("gale", "Gale53489*&h!")
mydb = mycol['account_info']
db2 = pymongo.MongoClient("47.97.219.39:27018")
mycol2 = db2["admindb"]
mycol2.authenticate("gale", "Gale53489*&h!")
mydb2 = mycol2['ios_ltv_do']
for i in mydb2.find():
    a = 0
    while True:
        a += 1
        _time = i['time'] + a*86400
        if _time > time.time():
            break
        if a <= 30 or a == 60 or a == 90 or a == 180:
            ltv_name = 'ltv%s' % a
            all_cash = 0
            for cash in mycol['cash_purchase_order'].find({'purchase_time': {'$lte': _time}, 'status': 2}):
                if cash['role_id'] in i['role_list']:
                    all_cash += cash['price']
            ltv_price = all_cash/float(i['account_all'])
            print ltv_price
            if mycol2['ios_ltv_counter'].find_one({'date': i['data']}):
                mycol2['ios_ltv_counter'].update_one({'date': i['data']}, {'$set': {ltv_name: ltv_price}})
                print 'updating'
            else:
                mycol2['ios_ltv_counter'].insert_one({'date': i['data'], ltv_name: ltv_price})
                print 'inserting'

# for i in result:
#     print i
# client = pymongo.MongoClient(["47.97.219.39:27018"])
# mydb2 = client["admindb"]
# mydb2 .authenticate("gale", "Gale53489*&h!")
# mycol2 = mydb2['dau_role_ios']
# mycol2.aggregate([{'$group': {'_id': '$role_name'}}])

# for role in mydb.find():
#     user_id = mycol2.find_one({'role_name': role['role_name']})['user_id']
#     account = mydb2['account_info'].find_one({'_id': ObjectId(str(user_id))})
#     mydb.update_one({'role_name': role['role_name']},
#                     {'$set': {'phone_number': account['account'],
#                               'channel_type': account['channel_type'],
#                               'channel_type_ex': account['channel_type_ex']
#                               }})
#     print account
# print 'ok'
# role_no = []
# role_all = []
# role_send = []
# for role in mydb.find({'primaryId': '31388ab0-f0b6-11e9-8e3e-00163f00186f'}):
#     print 1
#     role_all.append(role['role_id'])
# for role in mydb.find({'primaryId': 'cd577532-f197-11e9-b88e-00163f00186f'}):
#     print 2
#     role_send.append(role['role_id'])
# for i in role_all:
#     print 3
#     if i not in role_send:
#         role_no.append(i)
#
# print role_all
# print len(role_all)
# print role_send
# print len(role_send)
# print role_no
# print len(role_no)
#




# print 123
# email = mydb.find_one({'primaryId': '606d2e94-ef3a-11e9-a658-00163f00186f'})
# send_all = []
# send_ok = email['role_id']
# send_no = []
# for role in mydb2.find():
#     print 456
#     account = mycol2['account_info'].find_one({'_id': ObjectId(str(role['user_id']))})
#     if account['register_time'] < 1571135400:
#         send_all.append(str(role['_id']))
# for i in send_all:
#     print 789
#     if i not in send_ok:
#         print 000
#         send_no.append([i])
# print send_no
# print len(send_no)


# print email['content']
# print email['email_list']
# print len(email['email_list'])
#
# import time
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# mycol = client['admindb']
# mydb = mycol['test_insert']
# time1 = time.time()
# test_list = []
# for i in range(10000):
#     test_list.append({'name': i})
# mydb.insert_many(test_list)
# time2 = time.time()
# print time2 - time1

#
# mydb.update_many({"channel_type_ex": 5}, {"$set": {"channel_type_ex": 'vivo'}})
# mydb.update_many({"channel_type_ex": 13}, {"$set": {"channel_type_ex": 'uc'}})

#
# a = 0
# b = 0

# for role in mydb2.find():
#     if role['uid'] != '':
#         b += 1
#         six_role = mydb.find_one({'uid': role['uid']})
#         if six_role:
#             a += 1
#             print six_role['uid']
#         else:
#             role_name = mycol2['t1_role_data'].find_one({'user_id': str(role['_id'])})
#             if role_name:
#                 predict_num = 0
#                 cumulative_recharge = 0
#                 for cash in mycol2['t1_cash_purchase_order'].find({'role_id': str(role_name['_id']), 'status': 2}):
#                     cumulative_recharge += cash['price']
#                     if cash['price'] == 98 and cash['product_id'] in [11, 12, 13]:
#                         predict_num += 1
#                 print role['uid'], role_name['role_name'], predict_num, cumulative_recharge, \
#                     role['channel_type_ex'], role['channel_type']

# for cash in mycol2['t1_cash_purchase_order'].find({'status': 2}):
#     role = mycol2['t1_role_data'].find_one({'_id': cash['role_id']})
#     account = mydb2.find_one({'_id': role['user_id']})
#     if account['uid']:
#         if mydb.find_one({'uid': account['uid'], 'create_time': 6}):
#             mydb.update_one({'uid': account['uid']}, {'$inc': {'cumulative_recharge': cash['price']}})
#             if cash['price'] == 98 and cash['product_id'] in [11, 12, 13]:
#                 mydb.update_one({'uid': account['uid']}, {'$inc': {'predict_num': 1}})
#                 print 'ok'






# for role in mydb.find():
#     if role['uid'] != '':
#         b += 1
#         six_role = mydb2.find_one({'uid': role['uid']})
#         if six_role:
# #             a += 1
# print a
# print b

#             role_name = mycol2['t1_role_data'].find_one({'user_id': str(six_role['_id'])})
#             if role_name:
#                 for cash in mycol2['t1_cash_purchase_order'].find({'role_id': str(role_name['_id']), 'status': 2}):
#                     # print role_name['role_name'], cash['price'], cash['status'], cash['product_id']
#                     print role['uid']
#                     # mydb.update_one({'uid': role['uid']}, {'$inc': {'cumulative_recharge': cash['price']}})

# db = pymongo.MongoClient(["dds-bp128870cad650341168-pub.mongodb.rds.aliyuncs.com:3717"])
# mycol2 = db["game"]
# mycol2.authenticate("gale", "Gale53489*&h!")
# mydb2 = mycol2['account_info']

# a = 0
# for i in mydb.find():
#     a += i['predict_num']
# print a
# role_eight = []
# role_now = []
# for role in mycol2['role_data'].find():
#     cashs = mycol2['cash_purchase_order'].find({'role_id': str(role['_id'])})
#     for cash in cashs:
#         if cash and cash['price'] == 98 and cash['status'] == 2:
#             if cash['product_id'] in [11,12,13]:
#                 print role['role_name']
#                 role_eight.append(role['role_name'])
# for role in mydb.find():
#     role_now.append(role['role_name'])
#
# for h in role_eight:
#     if h not in role_now:
#         print '>>>>>>>>>>>>', h
# print role_now
# print len(role_now)
# print role_eight
# print len(role_eight)
# for account_1 in mydb.find():
#     if account_1['account']:
#         obj = mydb2.find_one({'account': account_1['account'], 'channel_type_ex': account_1['channel_type_ex']})
#         # mydb.update_one({'account': account_1['account'], 'channel_type_ex': account_1['channel_type_ex']},
#         #                 {'$set': {'predict_num': 0}})
#     else:
#         obj = mydb2.find_one({'uid': account_1['uid'], 'channel_type_ex': account_1['channel_type_ex']})
#         # mydb.update_one({'uid': account_1['uid'], 'channel_type_ex': account_1['channel_type_ex']},
#         #                 {'$set': {'predict_num': 0}})
#
#     role = mycol2['role_data'].find_one({'user_id': str(obj['_id'])})
#     if role:
#         cashs = mycol2['cash_purchase_order'].find({'role_id': str(role['_id'])})
#         for cash in cashs:
#             if cash['price'] == 98 and cash['status'] == 2:
#                 if cash['product_id'] in [11,12,13]:
#                     print cash['price'], cash['product_id'], cash['status']
#                     mydb.update_one({'_id': account_1['_id']}, {'$inc': {'predict_num': 1}})
#                     print cash['product_id'], cash['status']


# channel_list = []
# a = 0
# for i in mydb.find():
#     channel_list.append(i['channel_type'])
# channel_list = list(set(channel_list))
# print channel_list
# data = []
# for channel in channel_list:
#     result = 0
#     for i in mydb.find():
#         if i['channel_type'] == channel and i['status'] == 2:
#             result += i['price']
#     data.append({channel: result})
#
# print data






# def insert_db_many(table_name, db_list):
#     mycol[table_name].insert_many(db_list)
#
#
# def sdk_db(url, data):
#     result = json.loads(requests.post(url, data=data).text)
#     return result
#
#
# if __name__ == '__main__':
#     # url = 'https://m.lianhuigame.com/user/queryUser.json'
#     # url = 'https://m.lianhuigame.com/pay/queryOrder.json'
#     # url = 'https://m.lianhuigame.com//user/queryUser.json'
#     url = 'https://m.lianhuigame.com/user/queryRetentionUser.json'
#     data = {"startDate":'2019-08-21 16:13:00',"endDate":'2019-09-21 23:59:59','days':1}
#     # data2 = {}
#     result = sdk_db(url, data)
#     print result


# client = pymongo.MongoClient("mongodb://localhost:27017/")
# mycol = client['admindb']
# mydb = mycol['rebate_account']
# from tool.time_change import timestamp_to_time,time_to_timestamp,time_add,time_add_detail
# from bson import ObjectId
# # 连接后台数据库
# db_admin = pymongo.MongoClient(["47.97.219.39:27018"])
# mycol_admin = db_admin["admindb"]
# mycol_admin.authenticate("gale", "Gale53489*&h!")
#
# #  连接ios数据库
# db_ios = pymongo.MongoClient(["s-bp12fefdcdc7d3f4-pub.mongodb.rds.aliyuncs.com:3717"])
# mycol_ios = db_ios["game"]
# mycol_ios.authenticate("gale", "Gale53489*&h!")
#
# for i in mycol_admin['ios_day_data'].find({'date': {"$gte":'2019-09-03', "$lte": '2019-09-05'}}):
#     date_time = time_to_timestamp(i['date'])
#     all_pay = 0
#     all_pay_account = []
#     new_increase_limit = 0
#     new_increase_pay = []
#     for cash in mycol_ios['cash_purchase_order'].find({'purchase_time': {'$gte':date_time,'$lte':date_time+3600*24}, 'status':2}):
#         all_pay += cash['price']
#         all_pay_account.append(cash['role_id'])
#         role = mycol_ios['role_data'].find_one({'_id': ObjectId(cash['role_id'])})
#         account = mycol_ios['account_info'].find_one({'_id': ObjectId(role['user_id'])})
#         if date_time <= account['register_time'] <= date_time+3600*24:
#             new_increase_limit += cash['price']
#             new_increase_pay.append(cash['role_id'])
#     all_pay_account = len(set(all_pay_account))
#     new_increase_pay = len(set(new_increase_pay))
#     old_pay_account = all_pay_account - new_increase_pay
#     old_pay_account_limit = all_pay - new_increase_limit
#     print i['date'], all_pay, all_pay_account, new_increase_limit, new_increase_pay, old_pay_account_limit, old_pay_account
#     mycol_admin['ios_day_data'].update_one({'date': i['date']}, {'$set': {'all_pay': all_pay,
#                                                                           'all_pay_account': all_pay_account,
#                                                                           'new_increase_limit': new_increase_limit,
#                                                                           'new_increase_pay': new_increase_pay,
#                                                                           'old_pay_account_limit': old_pay_account_limit,
#                                                                           'old_pay_account': old_pay_account,
#                                                                           }})

# client = pymongo.MongoClient("mongodb://localhost:27017/")
# mycol = client['android_test']
# mydb = mycol['cash_purchase_order']
# a = 0
# b = 0
# c = []
# for i in mydb.find({'status': 2, 'channel_type': 'ssjj', 'purchase_time': {'$gte': 1566835200, '$lte': 1567008000}}):
#     b += 1
#     a += i['price']
#     c.append({'id': i['transaction_id'], 'price': i['price']})
# print a
# print b
# print c




