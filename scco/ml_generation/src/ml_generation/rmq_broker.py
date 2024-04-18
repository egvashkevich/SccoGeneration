import inspect
from typing import Callable

import pika
from pika.adapters.blocking_connection import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

import ml_generation.broker_config as bc


# TODO: add on_reply
class Publisher:
    def __init__(
            self,
            name: str,
            exchange: str,
            queue: str,
            routing_key: str,
    ):
        self.name = name
        self.exchange = exchange
        self.queue = queue
        self.routing_key = routing_key


class Consumer:
    def __init__(
            self,
            exchange: str,
            queue: str,
            routing_key: str,
            callback: Callable,
    ):
        self.exchange = exchange
        self.queue = queue
        self.routing_key = routing_key
        self.callback = callback


class RmqBroker:
    ############################################################################
    # API

    def __init__(self) -> None:
        self.chan = self.__class__._create_channel()
        self.pubs: dict[str, Publisher] = {}

    def add_publisher(self, publisher: Publisher):
        self.pubs[publisher.name] = publisher
        self.chan.exchange_declare(
            exchange=publisher.exchange,
            exchange_type='topic',
        )
        self.chan.queue_declare(
            queue=publisher.queue,
        )
        self.chan.queue_bind(
            exchange=publisher.exchange,
            queue=publisher.queue,
            routing_key=publisher.routing_key,
        )

    def add_consumer(self, consumer: Consumer):
        self.chan.exchange_declare(
            exchange=consumer.exchange,
            exchange_type='topic',
        )
        q = self.chan.queue_declare(
            queue=consumer.queue,
        )
        q_name = q.method.queue  # if consumer.queue == "" - auto generate queue
        consumer.queue = q_name
        self.chan.queue_bind(
            exchange=consumer.exchange,
            queue=consumer.queue,
            routing_key=consumer.routing_key,
        )
        self.chan.basic_consume(
            queue=consumer.queue,
            on_message_callback=consumer.callback,
        )

    def start_consuming(self):
        self.chan.start_consuming()  # Infinite loop.

    def basic_publish(self, publisher_name: str, body: bytes):
        if publisher_name not in self.pubs:
            RuntimeError(
                inspect.cleandoc(
                    f"""invalid publisher name
                    provided name: {publisher_name}
                    accessible names: {self.pubs.keys()}"""
                )
            )

        pub = self.pubs[publisher_name]
        self.chan.basic_publish(
            exchange=pub.exchange,
            routing_key=pub.routing_key,
            body=body,
        )

    ############################################################################
    # Internals

    # One connection for all service.
    _conn: BlockingConnection = pika.BlockingConnection(
        pika.ConnectionParameters(host=bc.RMQ_NET_ALIAS)
    )

    @classmethod
    def _create_channel(cls) -> BlockingChannel:
        chan = cls._conn.channel()
        return chan
