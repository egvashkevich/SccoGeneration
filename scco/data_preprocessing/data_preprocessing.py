import pandas as pd
import json
import os
import pika
import sys
from rabbit_rpc import FilterRpcClient
from emoji import replace_emoji

import config
from pipeline_operations import (
    ColumnTransform, StableSortBy, GroupBy, FilterAlreadySeen,
    FilterByTextMatch, InsertToDatabase, CommonMatchingList  # , CustomerMatchingList
)


class Preprocessor:
    def __init__(self):
        print(" [*] Initializing Preprocessor", flush=True)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.RABBIT_ADDRESS))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=config.IN_QUEUE, durable=True)
        self.channel.queue_declare(queue=config.OUT_QUEUE, durable=True)

        self.filter_rpc_client = FilterRpcClient(self.connection, self.channel)

        self.new_queries_csv_info = {'path': None}

        self.channel.basic_consume(queue=config.IN_QUEUE,
                                   on_message_callback=self.on_message_received)

    def start(self):
        print(" [*] Waiting for messages. To exit press CTRL+C", flush=True)
        self.channel.start_consuming()

    def on_message_received(self, ch, method, properties, body):
        print(f" [x] Received {body}", flush=True)

        try:
            json_in = json.loads(body.decode())

            data = pd.read_csv(json_in['parsed_csv'])
            data.columns = ['channel_id', 'client_id', 'message', 'message_date']
            customer_id = json_in['customer_id']
        except Exception as e:
            print(" [x] Caught the following exception when parsing input:")
            print(e)
            print(" [x] Sending ack, continue listening", flush=True)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        pipeline = [
            ColumnTransform('message', lambda s: replace_emoji(s, '')),
            ColumnTransform('message', str.lower),
            StableSortBy('message_date'),
            GroupBy(['channel_id', 'client_id', 'message_date'], agg={'message': (lambda x: list(x)[-1])}),
            # FilterAlreadySeen(by=['channel_id', 'client_id', 'message_date'],
            #                   customer_id=customer_id, on_nothing_left='all messages were already seen',
            #                   rpc_client=self.filter_rpc_client),
            # SaveNewQueries(self.new_queries_csv_info),
            FilterByTextMatch(CommonMatchingList(), mode='blacklist', algorithm='word',
                              on_nothing_left='all messages filtered out by common black list'),
            FilterByTextMatch(CommonMatchingList('resources/test_lists/trusted_strong_blacklist'), mode='blacklist',
                              on_nothing_left='all messages filtered out by common strong black list'),
            # FilterByTextMatch(CommonMatchingList('resources/test_lists/trusted_strong_whitelist'), mode='whitelist',
            #                   on_nothing_left='all messages filtered out by common strong white list'),
            FilterByTextMatch(CommonMatchingList('resources/test_lists/trusted_week_whitelist'), mode='whitelist',
                              on_nothing_left='all messages filtered out by common weak white list'),
            FilterByTextMatch(CommonMatchingList('resources/test_lists/trusted_week_blacklist'), mode='blacklist',
                              on_nothing_left='all messages filtered out by common weak black list'),
            # TODO week -> weak
            FilterByTextMatch(CommonMatchingList('resources/test_lists/user_blacklist'), mode='blacklist',
                              on_nothing_left='all messages filtered out by user black list'),
            # FilterByTextMatch(CommonMatchingList('resources/test_lists/user_whitelist'), mode='whitelist',
            #                   on_nothing_left='all messages filtered out by user white list'),
            # TODO these for users

            # FilterByBlackList(CommonBlackList(), on_nothing_left='all messages had words from common black list'),
            # FilterByBlackList(CustomerBlackList(customer_id),
            #                   on_nothing_left='all messages had words from customer\'s black list'),
            GroupBy(['client_id'], agg={'channel_id': list, 'message': list, 'message_date': list},
                    rename={'channel_id': 'channel_ids', 'message': 'messages', 'message_date': 'message_dates'}),
            # InsertToDatabase(customer_id=customer_id, new_queries_csv=new_queries_csv_path)
        ]

        for operation in pipeline:
            print(f'before op {type(operation)}', flush=True)
            print(f'{data=}', flush=True)
            data = operation(data)
            print(f'finished op {type(operation)}', flush=True)
            print(f'{data=}', flush=True)
            if data.empty:
                if hasattr(operation, 'on_nothing_left'):
                    print(' [x] Nothing to send further:', operation.on_nothing_left, flush=True)
                else:
                    raise ValueError('Nothing to send further, for an unpredicted reason')
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

        print(f" [x] Sending {len(data)} messages")
        with open('/data/new_queries/out.txt', 'w') as f:
            for index, row in data.iterrows():
                json_str = json.dumps({col: str(row[col]) for col in data.columns})
                # self.send_message(ch, json_str)
                print(json_str, file=f)
        print(" [x] Done", flush=True)

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
