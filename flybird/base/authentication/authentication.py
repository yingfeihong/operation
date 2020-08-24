# -*- coding: utf-8 -*-

""" 用户认证类 (Json Web Token方案，即JWT)
"""

import time
import functools
import base64
import json
from tornado.websocket import WebSocketHandler
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature, BadData
from config.global_variable import TOKEN_SECRET_KEY, ACCESS_TOKEN_EXPIRATION, REFRESH_TOKEN_EXPIRATION
from config.server_config import ServerConfig
from base.db.redis_manager import RedisManager
from share import action_status_code as code
from lang.chs import MESSAGE
from base.log.log_manager import LogManager as Log


def base64_decode(s):
    """Add missing padding to string and return the decoded base64 string."""
    s = str(s).strip()
    try:
        return base64.b64decode(s)
    except TypeError:
        padding = len(s) % 4
        if padding == 1:
            Log.logger.error("Invalid base64 string: {}".format(s))
            return ''
        elif padding == 2:
            s += b'=='
        elif padding == 3:
            s += b'='
        return base64.b64decode(s)


def pack_token_key(user_id, token_type):
    """
    组装角色token信息的键
    :param user_id:
    :param token_type:
    :return:
    """
    return "access:token:" + str(user_id) if token_type == "access" else "refresh:token:" + str(user_id)


def generate_token(user_id, token_type):
    """
    生成Token
    :param user_id:
    :param token_type:
    :return:
    """
    payload = {'user_id': user_id, 'iat': time.time(), 'version': ServerConfig.current_version}
    expire_time = ACCESS_TOKEN_EXPIRATION if token_type == 'access' else REFRESH_TOKEN_EXPIRATION
    # 生成token
    s = Serializer(secret_key=TOKEN_SECRET_KEY, expires_in=expire_time)
    token = s.dumps(payload).encode('utf-8')

    role_token_key = pack_token_key(user_id, token_type)
    RedisManager.cache_set(role_token_key, token, expire=expire_time)
    return token


def verify_token(token, token_type='access'):
    """
    验证Token
    :param token:
    :param token_type:
    :return:
    """
    user_id = get_token_user_id(token)
    Log.logger.info('verify token user_id is {}, token is {}'.format(user_id, token))
    token_info = RedisManager.get_cache(pack_token_key(user_id, token_type))
    if not token_info:
        return {'status': code.TOKEN_ERROR, 'data': {}, 'message': MESSAGE.get(code.TOKEN_ERROR)}
    s = Serializer(secret_key=TOKEN_SECRET_KEY)
    try:
        s.loads(token, return_header=True)
    except SignatureExpired:
        return {'status': code.TOKEN_EXPIRED, 'data': {}, 'message': MESSAGE.get(code.TOKEN_EXPIRED)}
    except BadSignature, e:
        encoded_payload = e.payload
        if encoded_payload:
            try:
                s.load_payload(encoded_payload)
            except BadData:
                return {'status': code.TOKEN_ERROR, 'data': {}, 'message': MESSAGE.get(code.TOKEN_ERROR)}
        return {'status': code.TOKEN_ERROR, 'data': {}, 'message': MESSAGE.get(code.TOKEN_ERROR)}
    except Exception as e:
        Log.logger.error("check token error is {}".format(e))
        return {'status': code.TOKEN_ERROR, 'data': {}, 'message': MESSAGE.get(code.TOKEN_ERROR)}
    if token != token_info:
        return {'status': code.TOKEN_ERROR, 'data': {},
                'message': MESSAGE.get(code.TOKEN_ERROR)}
    return {'status': 0, 'data': {'user_id': user_id}}


def get_header(token):
    """
    获取header
    :param token:
    :return:
    """
    s = Serializer(TOKEN_SECRET_KEY)
    return s.loads(token, return_header=True)[1]


def get_token_user_id(token):
    """
    获取token的角色id
    :param token:
    :return:
    """
    second_part_token = token.split('.')[1]
    Log.logger.info('second part token is:{}'.format(second_part_token))
    token_data = base64_decode(second_part_token)
    token_data = json.loads(token_data)
    user_id = token_data.get('user_id')
    return user_id


class AuthHandler(WebSocketHandler):
    def get_current_user(self):
        # token 验证
        token = self.request.headers.get("Authorization", None)
        role_id = get_token_user_id(token)
        if role_id:
            return role_id
        return None


class SocketAuthHandler(WebSocketHandler):
    def get_current_user(self):
        # token 验证
        Log.logger.info('begin verify token')
        token = self.get_argument('token')
        role_id = get_token_user_id(token)
        Log.logger.info('get current user:{}---------------'.format(role_id))
        if role_id:
            return role_id
        return None


def authentication(method):
    """Decorate methods with this to require that the user be logged in.

        If the user is not logged in, they will be redirected to the configured
        `login url <RequestHandler.get_login_url>`.

        If you configure a login url with a query parameter, Tornado will
        assume you know what you're doing and use it as-is.  If not, it
        will add a `next` parameter so the login page knows where to send
        you once you're logged in.
        """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            from base.network.user_request import UserRequest
            result = {'code': code.USER_NOT_EXIST, 'data': None}
            print self.request.headers.values()
            if 'websocket' in self.request.headers.values():
                self.write_message(UserRequest.handle_request_for_web_socket(result))
            else:
                result = json.dumps(result)
                self.write(UserRequest.pre_handle_response(result))
        else:
            return method(self, *args, **kwargs)
    return wrapper