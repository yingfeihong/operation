# -*- coding: utf-8 -*-

""" 消息队列
"""

from kafka import KafkaProducer
from kafka import KafkaConsumer
from config.server_config import ServerConfig


class MessageQueue(object):
    """ 消息队列
    """

    topic = ''

    @classmethod
    def init(cls):
        """ 初始化
        """
        pass

    @classmethod
    def get_consumer(cls, topic):
        """
        获得消费者数据
        :param topic:
        :return:
        """
        config_name = "test"
        section = "MessageQueueServer"
        field_address = "address"

        # Todo 需要先把zookeeper Kafka安装配置好
        consumer = KafkaConsumer(topic,
                                 bootstrap_servers=ServerConfig.get_server_info(config_name, section, field_address))
        return consumer

    @classmethod
    def send_msg(cls, topic, msg):
        """
        发送消息
        :param topic:
        :param msg:
        :return:
        """
        config_name = "test"
        section = "MessageQueueServer"
        field_address = "address"

        producer = KafkaProducer(bootstrap_servers=ServerConfig.get_server_info(config_name, section, field_address))
        producer.send(topic, msg)
