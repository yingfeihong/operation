# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: QL Liu
"""
import os
from celery import Celery
from core.init.celery import CeleryServerInit
from config.server_config import ServerConfig
env = os.getenv('ENV') or 'local'

# 初始化配置
CeleryServerInit.init(env)
# 创建celery实例 admin：实例名  broker：中间人  backend=backend include：任务函数路径
app = Celery('admin', include=["base.asyn.celery.task"], broker=ServerConfig.celery_config.get('broker'))
# 实例配置
app.config_from_object("base.asyn.celery.celeryconfig")


if __name__ == "__main__":
    app.start()
