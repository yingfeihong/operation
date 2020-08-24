# -*- coding: utf-8 -*-

"""
加密主要包括：账户的密码的加密、传输过程加密等。传输过程的加密的秘钥应该每次玩家登陆后，随机生成。
"""
import base64
import hashlib
from Crypto.Cipher import AES


def encrypt_text(text, secret_key):
    """
    加密
    :param text:
    :param secret_key: 密钥
    :return:
    """
    encrypted_text = encrypt_aes(text, secret_key, AES.MODE_CBC)  # 加密
    result = base64.b64encode(encrypted_text)  # base64编码

    return result


def decrypt_text(text, secret_key):
    """
    解密
    :param text:
    :param secret_key: 密钥
    :return:
    """
    encrypted_text = base64.b64decode(text)  # base64解码
    result = decrypt_aes(encrypted_text, secret_key, AES.MODE_CBC)  # 解密
    return result


def encrypt_aes(text, protocol_key, mode):
    """
    AES算法: 加密
    :param text:
    :param protocol_key:
    :param mode:
    :return:
    """
    iv = protocol_key  # 为了方便，直接使用protocol_key做为iv的值
    obj = AES.new(protocol_key, mode, iv)
    pad_it = lambda s: s + (16 - len(s) % 16) * '\0'
    result = obj.encrypt(pad_it(text.encode('utf-8')))
    return result


def decrypt_aes(text, protocol_key, mode):
    """
    AES算法: 解密
    :param text:
    :param protocol_key:
    :param mode:
    :return:
    """
    iv = protocol_key
    obj = AES.new(protocol_key, mode, iv)

    plain_text = obj.decrypt(text)
    result = plain_text.rstrip('\0')
    return result


def encrypt_md5(words, upper=False):
    """
    MD5 encryption words and return upper hashed string
    :param upper: 大写
    :param words: string
    :return: hashed_upper_string
    """
    m = hashlib.md5()
    m.update(words)
    hashed_words = m.hexdigest()
    if upper:
        return hashed_words.upper()
    return hashed_words.lower()


# print encrypt_md5('@12#%8743!YGa*&')
