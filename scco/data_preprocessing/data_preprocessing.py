import csv
import json
import os
import pika
import sys
import urllib.request

import config
from tools.dict_occurrence import DictOccurrenceManager


def add_to_database(dict_database):
    pass  # TODO: implement


def on_message_received(ch, method, properties, body):
    print(f" [x] Received {body}")

    json_in = json.loads(body.decode())
    customer_id = json_in['customer_id']
    csv_url = json_in['parsed_csv']

    source = csv_url
    if source.startswith('http'):
        source = urllib.request.Request(source)
    with urllib.request.urlopen(source) as f:
        data = f.read().decode().split('\n')

    data.pop(0)  # drop header

    words_black_list = config.COMMON_BLACK_LIST  # TODO get by customer_id
    occurrenceManager = DictOccurrenceManager(words_black_list)

    # TODO: group by (customer_id, client_id, channel_id)
    for channel_id, client_id, message, message_date in csv.reader(data):

        if occurrenceManager.check_occurrence_with_errors(message, 2):
            continue  # ignore this client

        dict_out = {
            'customer_id': customer_id,
            'client_id': client_id,
            'channel_id': channel_id,
            'message': message,
            'message_date': message_date
        }
        dict_database = {
            'customer_id': customer_id,
            'client_id': client_id,
            'channel_id': channel_id,
            'message_date': message_date
        }

        # TODO: check if already in database

        add_to_database(dict_database)
        send_message(ch, json.dumps(dict_out))

    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def send_message(channel, body):
    print(' [x] Sent a message')
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
