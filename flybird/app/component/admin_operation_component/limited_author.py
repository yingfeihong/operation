# -*- coding:utf-8 -*-
"""
Module Description:
Date:
Author: QL Liu
"""
from base.db.db_manager import DBManager
from bson import ObjectId


def limited_author(user_id):
    role = DBManager.get_record('admin_account', 'admindb', {'_id': ObjectId(user_id)})
    if len(role['show']) == 4:
        return True
    else:
        return False
