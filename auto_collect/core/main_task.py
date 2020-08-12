# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: Yfh
"""
from core.ssh_client import ssh
from lib.plugins import get_server_info


def task(host):
    result = get_server_info(ssh, host)
    print(result)