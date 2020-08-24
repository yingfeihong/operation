# -*- coding:utf-8 -*-
"""
Module Description:
Date: 2018-12-10
Author: QL Liu
"""
from __future__ import division
import time
from apscheduler.schedulers.tornado import TornadoScheduler
from app.component.admin_data_component.db_insert import cq_pay, cq_account,\
    cq_day, cq_ltv, msk_time_data, msk_ltv, day_insert, cq_account_time, cq_time_data,\
    android_msk_time_data, android_day_insert, android_msk_ltv, ios_ltv_counter, android_ltv_counter


def scheduler_jobs():
    """
    定时服务
    :return:
    """
    scheduler = TornadoScheduler()
    # 重置用于记录当天某些的变量
    # scheduler.add_job(cron_reset_daily_data, 'cron', day_of_week='0-6', hour=0, minute=0, second=0)
    # scheduler.add_job(scheduler_insert, 'interval', seconds=3600)
    # scheduler.add_job(scheduler_insert_type, 'interval', seconds=3600)
    # scheduler.add_job(all_insert, 'interval', seconds=10)

    scheduler.add_job(cq_pay, 'cron', hour='0-23')
    scheduler.add_job(cq_account, 'cron', hour='0-23')
    scheduler.add_job(cq_day, 'cron',  hour='0-23')
    scheduler.add_job(cq_ltv, 'cron',  hour='0-23')
    scheduler.add_job(cq_account_time, 'cron',  hour='0-23')
    scheduler.add_job(cq_time_data, 'cron',  hour='0-23')
    scheduler.add_job(msk_time_data, 'cron',  hour='0-23')
    scheduler.add_job(android_msk_time_data, 'cron',  hour='0-23')
    # scheduler.add_job(msk_ltv, 'cron', day_of_week='0-6', hour=23, minute=55, second=0)
    # scheduler.add_job(android_msk_ltv, 'cron', day_of_week='0-6', hour=23, minute=55, second=0)
    scheduler.add_job(day_insert, 'cron', day_of_week='0-6', hour=23, minute=55, second=0)
    scheduler.add_job(android_day_insert, 'cron', day_of_week='0-6', hour=23, minute=55, second=0)
    scheduler.add_job(ios_ltv_counter, 'cron', day_of_week='0-6', hour=23, minute=59, second=59)
    scheduler.add_job(android_ltv_counter, 'cron', day_of_week='0-6', hour=23, minute=59, second=59)
    # scheduler.add_job(test, 'cron', hour='0-23')
    # scheduler.add_job(dau_role, 'cron', day_of_week='0-6', hour=23, minute=55, second=0)
    return scheduler


def test():
    print 8888888888888888
    print time.time()
    print 9999999999999999


def cron_reset_daily_data():
    """
     定时更新角色数据(每日
    :return:
    """
    # DBManager.update_multi_property(DbTableConfig.table_user_data, {},
    #                                 {}, True)
    pass


