from typing import Callable

import pika
from pika.adapters.blocking_connection import (
    BlockingConnection,
    BlockingChannel,
)
from pika.channel import Channel

import util.parse_env as pe

# Getting environment variables.
RMQ_NET_ALIAS = pe.get("DB_FUNCTIONAL_SERVICE_NET_ALIAS")
DB_FUNCTIONAL_SERVICE_NET_ALIAS = pe.get("DB_FUNCTIONAL_SERVICE_NET_ALIAS")
DB_FUNCTIONAL_SERVICE_EXCHANGE = pe.get("DB_FUNCTIONAL_SERVICE_EXCHANGE")
DB_FUNCTIONAL_SERVICE_QUEUE = pe.get("DB_FUNCTIONAL_SERVICE_QUEUE")
DB_FUNCTIONAL_SERVICE_ROUTING_KEY = pe.get("DB_FUNCTIONAL_SERVICE_ROUTING_KEY")


class RmqHandle:
    conn: BlockingConnection = None
    chan: BlockingChannel = None
    callback: Callable = None

    @classmethod
    def _create_channel(cls) -> (BlockingConnection, Channel):
        cls.conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=RMQ_NET_ALIAS)
        )
        cls.chan = cls.conn.channel()

    @classmethod
    def _declare_exchange(cls):
        cls.chan.exchange_declare(
            exchange=DB_FUNCTIONAL_SERVICE_EXCHANGE,
            exchange_type='direct',
        )

    @classmethod
    def _declare_publish_queue(cls):
        pass

    @classmethod
    def _declare_consumer_queue(cls):
        # generated_offers queue.
        cls.chan.queue_declare(
            queue=DB_FUNCTIONAL_SERVICE_QUEUE
        )
        cls.chan.queue_bind(
            exchange=DB_FUNCTIONAL_SERVICE_EXCHANGE,
            queue=DB_FUNCTIONAL_SERVICE_QUEUE,
            routing_key=DB_FUNCTIONAL_SERVICE_ROUTING_KEY,
        )
        cls.chan.basic_consume(
            queue=DB_FUNCTIONAL_SERVICE_QUEUE,
            on_message_callback=cls.callback,
        )

    @classmethod
    def setup_rmq(cls, callback):
        cls.callback = callback

        conn, chan = cls._create_channel()
        cls._declare_exchange()
        cls._declare_consumer_queue()
        return chan

    @classmethod
    def start_consume(cls):
        cls.chan.start_consuming()  # Infinite loop.