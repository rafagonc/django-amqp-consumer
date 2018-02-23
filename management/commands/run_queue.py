from django.core.management.base import BaseCommand
from ...amqp import get_connection
from ...settings import log, find_queue_method


class CannotFindQueueNameParameterException(Exception):

    def __str__(self):
        return "Please provide the queue name by typing python manage.py run_queue {queue_name}"


class CannotDeclareQueueException(Exception):

    def __init__(self, queue, m):
        self.m = m
        self.queue = queue

    def __str__(self):
        return "Cannot declare queue:" + self.queue + " exception: " + self.m



def consume(method, queue_name, durable=True):
    connection = get_connection()
    channel = connection.channel()
    try:
        channel.queue_declare(queue=queue_name, durable=durable)
    except Exception as e:
        raise CannotDeclareQueueException(queue=queue_name, m=str(e))

    def callback(ch, m, properties, body):
        log("Received task on queue: " + queue_name)
        method(ch, m, properties, body)

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)
    log("Starting to consume queue named: " + queue_name)
    channel.start_consuming()


class Command(BaseCommand):

    help = "Run pika basic_consume with the desired queue"

    def handle(self, *args, **options):
        try:
            queue_name = options["queue"]
            durable = options.pop("durable", True)
        except:
            raise CannotFindQueueNameParameterException()
        method = find_queue_method(queue_name)
        consume(method, queue_name, durable)


    def add_arguments(self, parser):
        parser.add_argument(
            '--queue',
            action='store',
            dest='queue',
            help='''Name of the desired queue'''
        )

        parser.add_argument(
            '--durable',
            action='store',
            dest='durable',
            help='''If declare queue declare as durable'''
        )


