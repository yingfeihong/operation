# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: Yfh
"""
import requests

url = 'http://graduate.cmu.edu.cn/main_news_list.aspl'
result = requests.get(url, data={'lvid': 0201})
print result.text
