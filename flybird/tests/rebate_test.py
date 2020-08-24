# -*- coding:utf-8 -*-

from base.db.db_manager import DBManager
import requests
import json


def rebate():
    url = "http://47.97.219.39:9999/admin/login"
    # url = "http://192.168.188.16:9999/admin/login"
    url2 = "http://47.97.219.39:9999/admin/index"
    # url2 = "http://192.168.188.16:9999/admin/index"
    data = {"cmd": 2, "account": 'wzsy', "password": 123456}
    response = requests.post(url, data=json.dumps(data))
    print response.text
    a = json.loads(response.text)['data']['refreshToken']
    b = json.loads(response.text)['data']['accessToken']
    data2 = {"cmd": 9, 'data': {'account': '610731697', 'password': 'sbblg2586', 'role_name':'姜不听'}}
    response2 = requests.post(url2, data=json.dumps(data2), headers={'Authorization': b})
    print response2.text


if __name__ == '__main__':
    rebate()

