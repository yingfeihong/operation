# -*- coding:utf-8 -*-
import json
import requests

local = ["http://192.168.202.120:9999/admin/login", "http://192.168.202.120:9999/admin/index"]
prod = ["http://47.97.219.39:8888/admin/login", "http://47.97.219.39:8888/admin/index"]
develop = ["http://47.97.219.39:9999/admin/login", "http://47.97.219.39:9999/admin/index"]

login = {'cmd': 2, 'account': 'yfh2', 'password': 123456}
author = {'cmd': 10, 'data': {'type': 3, 'channel_name': '星魂-测试', 'company': '星魂'}}


def test_admin(env, module1=None, module2=None):
    response1 = requests.post(env[0], data=json.dumps(module1))
    print response1.text
    b = json.loads(response1.text)['data']['accessToken']
    response2 = requests.post(env[1], data=json.dumps(module2), headers={'Authorization': b})
    print response2.text


if __name__ == '__main__':
    test_admin(local, module1=login, module2=author)
    pass
