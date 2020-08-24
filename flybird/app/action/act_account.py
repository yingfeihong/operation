# -*- coding:utf-8 -*-
"""
Module Description:
Date: 2019-1-15
Author: QL Liu
"""
from share.action import LogAction
from app.component.admin_data_component.account_component import login, create_account, refresh_user_token
from app.constant.account import ACCOUNT_TYPE


class Login(LogAction):

    def do(self):
        return login(self.get('account'), self.get('password'))


class CreateAccount(LogAction):

    def before(self):

        if int(self.get('accountType')) not in [ACCOUNT_TYPE.ROOT, ACCOUNT_TYPE.COMMON]:
            return False
        return True

    def do(self):

        return create_account(self.get('account'), self.get('password'), self.get('accountType'))


class RefreshToken(LogAction):

    def do(self):
        return refresh_user_token(self.get('refreshToken'))

