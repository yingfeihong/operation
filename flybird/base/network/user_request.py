# -*- coding: utf-8 -*-

""" 客户端网络请求类
"""
import json
import time
from config.server_config import ServerConfig
from config.global_variable import IGNORE_PROTOCOL_LIST
from core.init.method_map import MethodMap
from base.authentication.authentication import verify_token
from base.log.log_manager import LogManager as Log
from share import action_status_code as code
from lang.chs import MESSAGE


def handle_request(request, message=None, post=True):
    """
    处理HTTP请求
    :param request: HTTP请求
    :param message: 客户端传过来的消息
    :param post:
    :return:
    """
    # 预处理http请求         (包括解密、解压缩等)
    pack_message, error = handle_request_message(request, message, post)
    if not error:
        request.write(pack_message)
        return True
    # 类地址
    class_address, error = get_class_address(request, pack_message)
    if not error:
        return False

    args = pack_args(request, pack_message)
    act = class_address(args)
    print 'args：', args
    print 'class_address：', class_address
    print 'act：', act
    result = act.take()
    Log.logger.info('result>>>>>:%s'%result)
    Log.logger.debug("process_result:%s", result)
    # 预处理返回值
    if result:
        request.write(result)
        if not result['status']:
            #  增加操作日志
            act.end_time = time.time()
            act.after()

    return True


def handle_request_message(request, message, post):
    """
    对http的消息进行预处理
    :param request:
    :param message:
    :param post:
    :return:
    """
    if post:
        pack_message, error = pre_handle_request(request.request.body)
    else:
        pack_message, error = message, True
    uri = request.request.uri.split('?')[0]
    # token 认证
    # check_result = check_token(request.request)
    if uri not in IGNORE_PROTOCOL_LIST:
        check_result = check_token(request.request)
        if check_result['status']:  # 参数有错误
            return check_result, False
        if error:
            pack_message['user_id'] = check_result['data']['user_id']
    return pack_message, error


def pre_handle_request(request_body):
    """
    预处理Http请求    e.g. 包括解密、解压缩等
    :param request_body:
    :return:
    """
    # 其他预处理等
    try:
        message = json.loads(request_body)
    except Exception as e:
        Log.logger.info("args need serialize, error:%s", e)
        return {'status': code.ARGS_NEED_SERIALIZE, 'data': None,
                'message': MESSAGE.get(code.ARGS_NEED_SERIALIZE)}, False
    return message, True


def check_token(request):
    """
    校验token
    :param request:
    :return:
    """
    # 用户验证 (JsonWebToken方案)
    token = request.headers.get("Authorization", None)
    if not token or token == 'null':
        return {'status': code.NO_TOKEN_FIELD, 'data': {}, 'message': MESSAGE.get(code.NO_TOKEN_FIELD)}
    res_data = verify_token(token)
    return res_data


def get_class_address(request, message):
    """
    获取客户端消息对应的处理类
    :param request:
    :param message:
    :return:
    """
    cmd = message.get('cmd')  # 从客户端获取
    Log.logger.info("cmd:%s", cmd)
    # 类地址
    class_address = MethodMap.map_classes.get(cmd)
    if not class_address:
        message = {'status': code.METHOD_NOT_FOUND, 'data': {}, 'message': MESSAGE.get(code.METHOD_NOT_FOUND)}
        request.write(message)
        return None, False
    return class_address, True


def pack_args(request, message):
    """
    组装请求参数
    :param request:
    :param message:
    :return:
    """
    if ServerConfig.config_name in ['test', 'prod']:
        remote_ip = request.request.headers.get('X-Forwarded-For', None)
    else:
        remote_ip = request.request.remote_ip
    message.update({'host_info': request.request.host, 'remote_ip': remote_ip})
    return message
