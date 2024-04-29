import pika
import json
import uuid
import config


class FilterRpcClient:
    def __init__(self, connection, channel):
        self.connection = connection
        self.channel = channel

        self.callback_queue = config.CONTAINS_QUERY_QUEUE
        self.channel.queue_declare(queue=self.callback_queue, durable=True)

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.reply_ctx = None
        self.response = None

    def on_response(self, ch, method, props, body):
        json_body = json.loads(body.decode())
        if self.reply_ctx == json_body['reply_ctx']:
            self.response = json_body['not_exist']

    def call(self, query_data):
        self.response = None
        self.reply_ctx = uuid.uuid4().hex
        request = json.dumps({
            "request_name": "filter_new_queries",
            "reply": {
                "exchange": config.CONTAINS_QUERY_EXCHANGE,
                "routing_key": config.CONTAINS_QUERY_ROUTING_KEY,
            },
            "reply_ctx": self.reply_ctx,
            "query_data": query_data
        })

        self.channel.basic_publish(
            exchange=config.DB_FUNCTIONAL_SERVICE_EXCHANGE,
            routing_key=config.DB_FUNCTIONAL_SERVICE_ROUTING_KEY,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            ),
            body=request)

        while self.response is None:
            self.connection.process_data_events(time_limit=None)
        return self.response
