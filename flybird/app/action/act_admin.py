# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: QL Liu
"""

from share.action import LogAction
from app.component.admin_data_component.admin_pay_component import index_pay
from app.component.admin_data_component.admin_time_component import index_time
from app.component.admin_data_component.admin_day_component import index_day
from app.component.admin_data_component.admin_ltv_component import index_ltv
from app.component.admin_data_component.admin_increase_component import index_increase
from app.component.admin_operation_component.admin_rebate import rebate
from app.component.super_admin_component import create_account
from app.component.admin_data_component.admin_leave import leave, dau
from app.component.admin_operation_component.announcement import announcement_do
from app.component.admin_operation_component.email import email
from app.component.admin_operation_component.banned import set_account_status, battle_error
from app.component.admin_operation_component.set_server import set_server_status


class IndexPay(LogAction):

    def do(self):
        return index_pay(self.get('data'))


class IndexTime(LogAction):
    def do(self):
        return index_time(self.get('data'))


class IndexLtv(LogAction):
    def do(self):
        return index_ltv(self.get('data'))


class IndexIncrease(LogAction):
    def do(self):
        return index_increase(self.get('data'))


class IndexDay(LogAction):
    def do(self):
        return index_day(self.get('data'))


class IndexRebate(LogAction):
    def do(self):
        return rebate(self.get('data'))


class SuperAdmin(LogAction):
    def do(self):
        return create_account(self.get('data'))


class Leave(LogAction):
    def do(self):
        return leave(self.get('data'))


class Dau(LogAction):
    def do(self):
        return dau(self.get('data'))


class Announcement(LogAction):
    def do(self):
        return announcement_do(self.get('data'))


class Email(LogAction):
    def do(self):
        return email(self.get('data'))


class Banned(LogAction):
    def do(self):
        return set_account_status(self.get('data'))


class ServerStatusSet(LogAction):
    def do(self):
        return set_server_status(self.get('data'))


class BattleError(LogAction):
    def do(self):
        return battle_error(self.get('data'))
