# -*- coding:utf-8 -*-
"""
Module Description:错误码
Date: 2018-4-11
Author: QL Liu
"""
# 后台 8000 ~ 8999
OK = 0
FAIL = 0
ARGS_ERROR = 8000  # 参数错误
USER_NOT_EXIST = 8001  # 用户不存在
METHOD_NOT_FOUND = 8002  # 方法没找到
ARGS_NEED_SERIALIZE = 8003  # 参数需要序列化
PASSWORD_ERROR = 8004  # 密码错误
TOKEN_ERROR = 8005  # token错误
TOKEN_EXPIRED = 8006  # token过期
ACCOUNT_LOGIN_OTHER_DEVICE = 8007  # 账号在其他设备登录
NO_TOKEN_FIELD = 8008  # 没有token字段
THE_ACCOUNT_EXIST = 8009   # 该账户已存在
CREATE_SUCCESS = 8888  # 创建成功
DELETE_SUCCESS = 8889  # 删除成功
UPDATA_SUCCESS = 8890  # 修改成功
UPDATA_AD = 9000  # 更新公告
INSERT_AD = 9001  # 插入公告
AD_HAVE = 9002  # 公告已存在
EMAIL_SEND = 9003  # 邮件发送成功
EMAIL_NOT = 9004  # 邮件未找到
EMAIL_DEL = 9005  # 邮件删除成功
ANNOUNCEMENT_CONTENT_NOT_BE_NULL = 9006  # 公告不能为空
ANNOUNCEMENT_INSERT = 9007  # 添加公告成功
END_TIME_SHOULD_BE_GREATER_THAN_START_TIME = 9008  # 传入时间不对
ANNOUNCEMENT_DELETE = 9009  # 删除公告成功
ANNOUNCEMENT_NOT_EXIST = 9010  # 公告未存在
THE_USER_HAS_BEEN_BAN_STATUS = 9011  # 用户已经是当前状态
SET_STATUS_SUCCESS = 9012  # 设置状态成功
ANNOUNCEMENT_UPDATE = 9013  # 修改公告成功
ITEM_NOT_FOUND = 9014  # 道具不存在
DATA_ERROR = 9015  # 传入数据有误
ROLE_NOT_EXIT = 9016  # 角色不存在
PRIMARY_NOT_HAVE = 9017  # 邮件id不存在
ROLL_FAILED = 9018  # 滚动公告发送失败
LEAVE_FAILED = 9019  # 第三方留存接口錯誤
DAU_FAILED = 9020  # 第三方dau接口錯誤
CLOSE_SERVER_FAIL = 9021  # 服务器关闭失败
ROOT_ACCOUNT_CAN_ONLY_HAVE_ONE = 8010  # 超级管理员只能有一个
AUTHOR_NOT = 8011  # 超级管理员只能有一个
# 网关
SEVER_IN_MAINTENANCE = 2000
ACCOUNT_IN_BAN_STATUS = 1021  # 账户被封





