# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: Yfh
"""
import redis
client = redis.Redis()
client.set('yfh:test2', [{'a': 1, 'b': 2}])