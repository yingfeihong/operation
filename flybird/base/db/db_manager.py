# -*- coding: utf-8 -*-

""" 数据库管理类的高层接口
"""
from bson import ObjectId
from base.db.db_util import DBUtil


class DBManager(object):
    """ 数据库管理类的高层接口
    符号含义示例
    $lt小于{'age': {'$lt': 20}}
    $gt大于{'age': {'$gt': 20}}
    $lte小于等于{'age': {'$lte': 20}}
    $gte大于等于{'age': {'$gte': 20}}
    $ne不等于{'age': {'$ne': 20}}
    $in在范围内{'age': {'$in': [20, 23]}}
    $nin不在范围内{'age': {'$nin': [20, 23]}}
    """

    @classmethod
    def get_record(cls, table_name, db_name, index_condition):
        """
        获得表中一条记录的数据
        :param table_name:
        :param db_name:
        :param index_condition:
        :return :
        """

        db = DBUtil.get_db_instance(db_name)
        result = db[table_name].find_one(index_condition)
        return result

    @classmethod
    def get_multi_record(cls, table_name, db_name, index_condition=None):
        """
        获取多条记录数据
        :param table_name:
        :param db_name:
        :param index_condition:
        :return:
        """
        db = DBUtil.get_db_instance(db_name)
        result = db[table_name].find(index_condition)
        return result

    @classmethod
    def get_multi_record_limit(cls, table_name, db_name, index_condition=None, limit=30, skip=0):
        """
        获取多条记录数据
        :param table_name:
        :param db_name:
        :param index_condition:
        :param limit:
        :param skip:
        :return:
        """
        db = DBUtil.get_db_instance(db_name)
        result = db[table_name].find(index_condition).sort('_id', -1).limit(limit).skip(skip)
        return result

    @classmethod
    def get_multi_record_count(cls, table_name, db_name, index_condition=None):
        """
        获取统计数据
        :param table_name:
        :param index_condition:
        :return:
        """
        db = DBUtil.get_db_instance(db_name)
        result = db[table_name].find(index_condition)
        a = 0
        for i in result:
            a += 1
        return a

    @classmethod
    def insert_record(cls, table_name, db_name, record, session=None):
        """
        向表中插入一条记录的数据
        :param table_name:
        :param record:
        :param session:
        :return :
        """
        db = DBUtil.get_db_instance(db_name)
        result = db[table_name].insert_one(record, session=session)
        if isinstance(result.inserted_id, ObjectId):
            return result.inserted_id
        return None

    @classmethod
    def get_property(cls, table_name,db_name, item_id, field):
        """
        获得属性
        :param table_name:
        :param item_id:
        :param field:
        :return :
        """
        db = DBUtil.get_db_instance(db_name)
        parameters = {'_id': item_id}

        result = db[table_name].find_one(parameters)

        return result[field]

    @classmethod
    def update_property(cls, table_name, db_name, index_condition, field, value, multi=False):
        """
        设置属性
        :param table_name:
        :param index_condition:
        :param field: 	字段
        :param value: 该字段新的值
        :param multi:
        :return:
        """
        db = DBUtil.get_db_instance(db_name)
        update = {'$set': {field: value}}

        result = db[table_name].update(index_condition, update, multi=multi)
        return result.get('updatedExisting')

    @classmethod
    def update_multi_property(cls, table_name,db_name, index_condition, update_content, multi=False):
        """
        更新多个字段
        :param table_name:
        :param index_condition:
        :param update_content:
        :param multi:
        :return:
        """
        db = DBUtil.get_db_instance(db_name)
        update = {'$set': update_content}
        result = db[table_name].update(index_condition, update, multi=multi)
        return result.get('updatedExisting')

    @classmethod
    def update_many(cls, table_name, db_name, index_condition, update_content, session=None):
        """
        更新符合条件的所有记录
        :param table_name:
        :param index_condition:
        :param update_content:
        :param session:
        :return:
        """
        db = DBUtil.get_db_instance(db_name)
        update = {'$set': update_content}
        db[table_name].update_many(index_condition, update, session=session)
        # print "result:", result
        # return result.get('updatedExisting')

    @classmethod
    def update_one(cls, table_name, db_name, index_condition, update_content, session=None):
        """
        更新符合条件的一条记录
        :param table_name:
        :param index_condition:
        :param update_content:
        :param session:
        :return:
        """
        db = DBUtil.get_db_instance(db_name)
        update = {'$set': update_content}
        db[table_name].update_one(index_condition, update, session=session)
        # print "result:", result.raw_result
        # return result.get('updatedExisting')

    @classmethod
    def inc_property(cls, table_name,db_name, index_condition, field, value, session=None):
        """
        设置属性, 采用mongodb的inc操作，对某个字段(int型)增加
        :param table_name:
        :param item_id:
        :param field:
        :param value:
        :param session:
        :return:
        """
        db = DBUtil.get_db_instance(db_name)
        # parameters = {'_id': item_id}
        parameters = index_condition
        update = {'$inc': {field: value}}

        db[table_name].update_one(parameters, update, session=session)

    @classmethod
    def delete_record(cls, table_name, db_name, index_condition, multi=False, session=None):
        """
        删除记录
        :param table_name:
        :param index_condition:
        :param multi: True:删除所有符合条件的记录, False:删除符合条件的一条记录
        :param session:
        :return:
        """
        db = DBUtil.get_db_instance(db_name)
        if not multi:
            db[table_name].delete_one(index_condition, session=session)
        else:
            db[table_name].delete_many(index_condition, session=session)

    @classmethod
    def remove_record(cls, table_name,db_name, index_condition, multi=False):
        """
        移除记录
        :param table_name:
        :param index_condition:
        :param multi:
        :return:
        """
        db = DBUtil.get_db_instance(db_name)
        db[table_name].remove(index_condition, multi=multi)

    @classmethod
    def get_given_filed_record(cls, table_name, db_name, index_condition, field, ascending=False):
        """
        获取指定字段最大值的记录
        :param table_name:
        :param index_condition:
        :param field:
        :param ascending: True:升序， False:降序
        :return:
        """
        db = DBUtil.get_db_instance(db_name)

        order = 1 if ascending else -1
        result = db[table_name].find(index_condition).sort(field, order)[0]
        return result
