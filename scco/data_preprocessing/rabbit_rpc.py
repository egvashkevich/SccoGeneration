import pika
import json
import uuid
import config


class FilterRpcClient:
    def __init__(self, connection, channel):
        self.connection = connection
        self.channel = channel

        self.callback_queue = config.CONTAINS_QUERY_QUEUE
        self.channel.queue_declare(queue=self.callback_queue, durable=True)  # TODO exchnge

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

    def call(self, request_data):
        self.response = None
        self.reply_ctx = uuid.uuid4().hex
        request = json.dumps({
            "request_name": "filter_new_queries",
            "reply": {
                "exchange": config.CONTAINS_QUERY_EXCHANGE,
                "routing_key": config.CONTAINS_QUERY_ROUTING_KEY,
            },
            "reply_ctx": self.reply_ctx,
            "request_data": request_data
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


class SaveCsvRpcClient:
    def __init__(self, connection, channel, new_queries_csv_info):
        self.connection = connection
        self.channel = channel

        self.callback_queue = config.INSERT_BEFORE_PREPROCESSING_QUERY_QUEUE  # TODO exchnge
        self.channel.queue_declare(queue=self.callback_queue, durable=True)

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)  # TODO auto_ack

        self.new_queries_csv_info = new_queries_csv_info
        self.response = None

    def on_response(self, ch, method, props, body):
        json_body = json.loads(body.decode())
        if self.new_queries_csv_info['path'] == json_body['reply_ctx']:  # TODO
            self.response = json_body['not_exist']

    def call(self, request_data):  # TODO
        self.response = None
