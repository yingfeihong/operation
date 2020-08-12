# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: Yfh
"""


class BasePlugin(object):

    def process(self, ssh, hostname):
        raise NotImplementedError('{}中必须实现process方法'.format(self.__class__.__name__))
