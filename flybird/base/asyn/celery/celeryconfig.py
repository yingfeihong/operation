# -*- coding:utf-8 -*-
"""
Module Description:
Date: 
Author: QL Liu
"""
from kombu import Queue, Exchange
CELERY_TASK_SERIALIZER = 'msgpack'
CELERY_RESULT_SERIALIZER = 'msgpack'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
CELERY_MESSAGE_COMPRESSION = 'zlib'
CELERYD_PREFETCH_MULTIPLIER = 4
CELERY_ACCEPT_CONTENT = ['json', 'msgpack']

exchange = Exchange('admin', type='direct')

CELERY_QUEUES = (
    Queue('emailsend', exchange, routing_key='admin_emailsend'),
    Queue('android_email', exchange, routing_key='route_android_email'),
    Queue('roll_send', exchange, routing_key='route_roll_send')
)
CELERY_ROUTES = {
        'base.asyn.celery.task.update_email_data': {
        'queue': 'emailsend',
        'routing_key': 'admin_emailsend'
    },
    'base.asyn.celery.task.update_email_data_android': {
        'queue': 'android_email',
        'routing_key': 'route_android_email'
    },
    'base.asyn.celery.task.roll': {
        'queue': 'roll_send',
        'routing_key': 'route_roll_send'
    }
}
