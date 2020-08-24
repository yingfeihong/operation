# -*- coding:utf-8 -*-

import requests
import json
import time
import pymongo
from bson import ObjectId

# db = pymongo.MongoClient(["s-bp1b263efa9a44e4-pub.mongodb.rds.aliyuncs.com:3717"])
# mycol = db["game"]
# mycol.authenticate("gale", "Gale53489*&h!")
# mydb = mycol['account_info']
# role_list = []
# for i in mydb.find({'channel_type_ex': 'huawei'}):
#     role = mycol['role_data'].find_one({'user_id': str(i['_id'])})
#     if role:
#         role_list.append(role['role_name'])
# print len(role_list)

def do_test_pay():
    # print 'open'
    # r = requests.post('192.168.200.144:9999/admin/login', json.dumps({'cmd': 2, 'account': 'yfh', 'password':123456}))
    # print r.text
    # print 'success'
    # headers = {
    #     "Content-Type": "application/json; charset=UTF-8"
    # }
    url = "http://47.97.219.39:8888/admin/login"
    # url = "http://47.97.219.39:9999/admin/login"
    # url = "http://192.168.1.116:9999/admin/login"
    # url2 = "http://192.168.1.116:9999/admin/index"
    # url2 = "http://47.97.219.39:9999/admin/index"
    url2 = "http://47.97.219.39:8888/admin/index"
    data = {"cmd": 2, "account": '应飞鸿', "password": 123456}
    response = requests.post(url, data=json.dumps(data))
    print response
    print type(response.status_code)
    print response.text
    # b = json.loads(response.text)['data']['accessToken']
    # a = json.loads(response.text)['data']['user_id']
    # data2 = {'cmd': 7, 'data': {'gameName': '马赛克英雄', 'channelName': 'mumayi'}}
    # response2 = requests.post(url2, data=json.dumps(data2), headers={'Authorization': b})
    # print json.loads(response2.text)


# 创建管理员用户>> 1
def create_account():
    data = {'account': '应飞鸿', 'password': '123456', 'accountType': 1, 'cmd': 1}
    url = "http://192.168.188.16:9999/admin/account/create"
    response = requests.post(url, data=json.dumps(data))
    print json.loads(response.text)


if __name__ == '__main__':
    do_test_pay()


