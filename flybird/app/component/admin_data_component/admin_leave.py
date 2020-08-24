# -*- coding:utf-8 -*-
"""
Module Description:
Date:
Author: QL Liu
"""

import requests
import json
from base.log.log_manager import LogManager as Log
from share import action_status_code as code


def leave(data):
    url = 'https://m.lianhuigame.com/user/queryRetentionUser.json'
    if data:
        try:
            result = json.loads(requests.post(url, data=data).text)
        except Exception as e:
            Log.logger.info("leave data fail, error is {}".format(e))
            return code.LEAVE_FAILED
        return result


def dau(data):
    url = 'https://m.lianhuigame.com/user/queryActiveUser.json'
    if data:
        try:
            result = json.loads(requests.post(url, data=data).text)
        except Exception as e:
            Log.logger.info("adu data fail, error is {}".format(e))
            return code.DAU_FAILED
        return result
