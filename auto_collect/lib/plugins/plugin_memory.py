# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: Yfh
"""
from .plugin_base import BasePlugin


class MemoryPlugin(BasePlugin):

    def process(self, ssh, hostname):
        result = ssh(hostname, 'free')
        return result
