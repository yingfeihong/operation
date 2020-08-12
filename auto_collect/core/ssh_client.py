# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: Yfh
"""
import paramiko
import settings


def ssh(hostname, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=22, username=settings.username, password=settings.password)
    stdin, stdout, stderr = client.exec_command(cmd)
    result = stdout.read().decode('utf-8')
    client.close()
    return result
