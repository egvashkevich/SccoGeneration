import pandas as pd
import json
import os
import pika
import sys
from emoji import replace_emoji

import config
from pipeline_operations import (
    ColumnTransform, StableSortBy, GroupBy, FilterAlreadySeen,
    FilterByBlackList, InsertToDatabase, CommonBlackList, CustomerBlackList
)


def on_message_received(ch, method, properties, body):
    print(f" [x] Received {body}")

    json_in = json.loads(body.decode())

    data = pd.read_csv(json_in['parsed_csv'])
    data.columns = ['channel_id', 'client_id', 'message', 'message_date']
    customer_id = json_in['customer_id']

    pipeline = [
        ColumnTransform('message', lambda s: replace_emoji(s, '')),
        ColumnTransform('message', str.lower),
        StableSortBy('message_date'),
        GroupBy(['channel_id', 'client_id', 'message_date'], agg={'message': (lambda x: list(x)[-1])}),
        FilterAlreadySeen(by=['channel_id', 'client_id', 'message_date'],
                          customer_id=customer_id, on_nothing_left='all messages were already seen'),
        FilterByBlackList(CommonBlackList(), on_nothing_left='all messages had words from common black list'),
        FilterByBlackList(CustomerBlackList(customer_id),
                          on_nothing_left='all messages had words from customer\'s black list'),
        GroupBy(['client_id', 'channel_id'], agg={'message': list, 'message_date': list},
                rename={'message': 'messages', 'message_date': 'message_dates'}),
        InsertToDatabase(customer_id=customer_id)
    ]

    for operation in pipeline:
        data = operation(data)
        if data.empty:
            if hasattr(operation, 'on_nothing_left'):
                print(' [x] Nothing to send further:', operation.on_nothing_left)
            else:
                raise ValueError('Nothing to send further, for an unpredicted reason')
            break
    else:
        print(f" [x] Sending {len(data)} messages")
        for index, row in data.iterrows():
            json_str = json.dumps({col: str(row[col]) for col in data.columns})
            send_message(ch, json_str)
        print(" [x] Done")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def send_message(channel, body):
    channel.basic_publish(exchange="", routing_key=config.OUT_QUEUE, body=body,
                          properties=pika.BasicProperties(
                              delivery_mode=pika.DeliveryMode.Persistent
                          ))


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.RABBIT_ADDRESS))
    channel = connection.channel()

    channel.queue_declare(queue=config.IN_QUEUE, durable=True)
    channel.queue_declare(queue=config.OUT_QUEUE, durable=True)

    channel.basic_consume(queue=config.IN_QUEUE,
                          on_message_callback=on_message_received)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


try:
    main()
except KeyboardInterrupt:
    print("Interrupted")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
