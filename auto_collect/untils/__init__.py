# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: Yfh
"""

from random import Random
import time
# t = 1597454400
b = [i for i in range(1, 13)]
# while True:
#     ex = None
#     a = Random(t)
#     if a.sample(b, 5) == [2, 1, 11, 9, 3]:
#         timeArray = time.localtime(t)
#         print('一', t, time.strftime("%Y--%m--%d %H:%M:%S", timeArray))
#     if a.sample(b, 5) == [1, 5, 10, 9, 11]:
#         timeArray = time.localtime(t)
#         print('二', t, time.strftime("%Y--%m--%d %H:%M:%S", timeArray))
#     if a.sample(b, 5) == [4, 7, 12, 11, 10]:
#         timeArray = time.localtime(t)
#         print('三', t, time.strftime("%Y--%m--%d %H:%M:%S", timeArray))
#     if a.sample(b, 5) == [12, 4, 5, 7, 11]:
#         timeArray = time.localtime(t)
#         print('四', t, time.strftime("%Y--%m--%d %H:%M:%S", timeArray))
#     if a.sample(b, 5) == [11, 1, 4, 7, 9]:
#         timeArray = time.localtime(t)
#         print('五', t, time.strftime("%Y--%m--%d %H:%M:%S", timeArray))
#     if a.sample(b, 5) == [8, 2, 4, 6, 9]:
#         timeArray = time.localtime(t)
#         print('六', t, time.strftime("%Y--%m--%d %H:%M:%S", timeArray))
#     if a.sample(b, 5) == [7, 8, 3, 10, 6]:
#         timeArray = time.localtime(t)
#         print('七', t, time.strftime("%Y--%m--%d %H:%M:%S", timeArray))
#     if a.sample(b, 5) == [7, 8, 9, 2, 10]:
#         timeArray = time.localtime(t)
#         print('八', t, time.strftime("%Y--%m--%d %H:%M:%S", timeArray))
#     if a.sample(b, 5) == [3, 9, 4, 10, 5]:
#         timeArray = time.localtime(t)
#         print('九', t, time.strftime("%Y--%m--%d %H:%M:%S", timeArray))
#     t += 1

# print(1597815034 - 1597658323)
# print(1597817326-1597815034)
print((1598867646-1598347789)/8)
t = 1598867646
for i in range(100000000):
    a = Random(t+i)
    if a.sample(b, 5) == [6, 4, 8, 9 , 1]:
        print(t, i)
        c = Random(t+i+i)
        print(c.sample(b, 5))
        break


