from django.test import TestCase
from .management.commands.run_queue import consume
from .amqp import get_connection
import pytest

# Create your tests here.


class TestQueueConsume:

    def test(self):
        conn = get_connection()
        channel = conn.channel()
        channel.basic_publish(exchange='',
                              routing_key="test_queue",
                              body="TEST")

        received = False

        def callback(ch, m, properties, body):
            nonlocal received
            received = True
            ch.stop_consuming()

        consume(callback, "test_queue", False)

        assert received == True