from django.conf import settings
from importlib import import_module
from .exceptions import CannotFindQueueException
import six

STATIC_QUEUE_RABBITMQ_HOST = settings.STATIC_QUEUE_RABBITMQ_HOST
STATIC_QUEUE_RABBITMQ_USER = settings.STATIC_QUEUE_RABBITMQ_USER
STATIC_QUEUE_RABBITMQ_VHOST = getattr(settings, 'STATIC_QUEUE_RABBITMQ_VHOST', "/")
STATIC_QUEUE_RABBITMQ_PASS = settings.STATIC_QUEUE_RABBITMQ_PASS
STATIC_QUEUE_RABBITMQ_LOG_CONNECTION = getattr(settings, 'STATIC_QUEUE_RABBITMQ_LOG_CONNECTION', True)
STATIC_QUEUE_RABBITMQ_QUEUES = settings.STATIC_QUEUE_RABBITMQ_QUEUES
STATIC_QUEUE_RABBITMQ_MAX_RETRYS = getattr(settings, 'STATIC_QUEUE_RABBITMQ_MAX_RETRYS', 10)


def find_queue_method(queue_name):
    queues = STATIC_QUEUE_RABBITMQ_QUEUES
    for q in queues:
        if q == queue_name:
            method = perform_import(queues[q])
            return method
    raise CannotFindQueueException(queue_name)


def perform_import(val):
    """

    Thanks rest-framework for this import method

    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, six.string_types):
        return import_from_string(val)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item) for item in val]
    return val


def import_from_string(val):
    """

    Thanks rest-framework for this import method

    Attempt to import a class from a string representation.
    """
    try:
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = "Could not import queue methods: " + str(e)
        raise ImportError(msg)


def log(m):
    if STATIC_QUEUE_RABBITMQ_LOG_CONNECTION:
        print(m)