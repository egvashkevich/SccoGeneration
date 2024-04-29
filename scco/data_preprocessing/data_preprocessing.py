import pandas as pd
import json
import os
import pika
import sys
import datetime
import uuid
from rabbit_rpc import FilterRpcClient
from emoji import replace_emoji

import config
from pipeline_operations import (
    ColumnTransform, StableSortBy, GroupBy, FilterAlreadySeen,
    FilterByBlackList, InsertToDatabase, CommonBlackList, CustomerBlackList
)


class Preprocessor:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.RABBIT_ADDRESS))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=config.IN_QUEUE, durable=True)
        self.channel.queue_declare(queue=config.OUT_QUEUE, durable=True)

        self.filter_rpc_client = FilterRpcClient(self.connection, self.channel)

        self.channel.basic_consume(queue=config.IN_QUEUE,
                                   on_message_callback=self.on_message_received)

    def start(self):
        print(" [*] Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def on_message_received(self, ch, method, properties, body):
        print(f" [x] Received {body}")

        json_in = json.loads(body.decode())

        data = pd.read_csv(json_in['parsed_csv'])
        data.columns = ['channel_id', 'client_id', 'message', 'message_date']
        customer_id = json_in['customer_id']

        pipeline1 = [
            ColumnTransform('message', lambda s: replace_emoji(s, '')),
            ColumnTransform('message', str.lower),
            StableSortBy('message_date'),
            GroupBy(['channel_id', 'client_id', 'message_date'], agg={'message': (lambda x: list(x)[-1])}),
            FilterAlreadySeen(by=['channel_id', 'client_id', 'message_date'],
                              customer_id=customer_id, on_nothing_left='all messages were already seen',
                              rpc_client=self.filter_rpc_client)
        ]

        for operation in pipeline1:
            data = operation(data)
            if data.empty:
                if hasattr(operation, 'on_nothing_left'):
                    print(' [x] Nothing to send further:', operation.on_nothing_left)
                else:
                    raise ValueError('Nothing to send further, for an unpredicted reason')
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

        today = datetime.date.today().strftime('%y-%m-%y')  # yyyy-mm-dd
        unique_id = uuid.uuid4().hex  # unique sting of hex symbols
        new_queries_csv_name = f'new-queries-{today}-{unique_id}.csv'
        os.makedirs(config.NEW_QUERIES_CSV_FOLDER, exist_ok=True)
        data.to_csv(os.path.join(config.NEW_QUERIES_CSV_FOLDER, new_queries_csv_name))
        new_queries_csv_path = config.NEW_QUERIES_PREFIX_FOR_SENDING + new_queries_csv_name

        # insert_csv_path_do_db(new_queries_csv_path)

        pipeline2 = [
            FilterByBlackList(CommonBlackList(), on_nothing_left='all messages had words from common black list'),
            FilterByBlackList(CustomerBlackList(customer_id),
                              on_nothing_left='all messages had words from customer\'s black list'),
            GroupBy(['client_id'], agg={'channel_id': list, 'message': list, 'message_date': list},
                    rename={'channel_id': 'channel_ids', 'message': 'messages', 'message_date': 'message_dates'}),
            InsertToDatabase(customer_id=customer_id, new_queries_csv=new_queries_csv_path)
        ]

        for operation in pipeline2:
            data = operation(data)
            if data.empty:
                if hasattr(operation, 'on_nothing_left'):
                    print(' [x] Nothing to send further:', operation.on_nothing_left)
                else:
                    raise ValueError('Nothing to send further, for an unpredicted reason')
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

        print(f" [x] Sending {len(data)} messages")
        for index, row in data.iterrows():
            json_str = json.dumps({col: str(row[col]) for col in data.columns})
            self.send_message(ch, json_str)
        print(" [x] Done")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def send_message(slef, channel, body):
        channel.basic_publish(exchange=config.ML_GENERATION_EXCHANGE,
                              routing_key=config.ML_GENERATION_ROUTING_KEY,
                              body=body,
                              properties=pika.BasicProperties(
                                  delivery_mode=pika.DeliveryMode.Persistent
                              ))


try:
    Preprocessor().start()
except KeyboardInterrupt:
    print("Interrupted")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
