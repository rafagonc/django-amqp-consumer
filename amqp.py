from pika import (BlockingConnection,
                  ConnectionParameters,
                  PlainCredentials)
from .settings import (STATIC_QUEUE_RABBITMQ_HOST,
                       STATIC_QUEUE_RABBITMQ_PASS,
                       STATIC_QUEUE_RABBITMQ_USER,
                       STATIC_QUEUE_RABBITMQ_VHOST,
                       STATIC_QUEUE_RABBITMQ_MAX_RETRYS,
                       log)


class CannotConnectException(Exception):

    def __str__(self):
        return "Cannot connect to amqp host: " + STATIC_QUEUE_RABBITMQ_HOST


def get_connection():
    count = 0
    while True:
        try:
            connc = BlockingConnection(ConnectionParameters(host=STATIC_QUEUE_RABBITMQ_HOST,
                                                            virtual_host=STATIC_QUEUE_RABBITMQ_VHOST,
                                                            credentials=PlainCredentials(username=STATIC_QUEUE_RABBITMQ_USER,
                                                                                         password=STATIC_QUEUE_RABBITMQ_PASS)))
            if connc.is_open:
                break
        except Exception as e:
            log("Connection problem - " + str(e) + " - Retrying...")
            count += 1
            if count >= STATIC_QUEUE_RABBITMQ_MAX_RETRYS:
                raise CannotConnectException()
    return connc


