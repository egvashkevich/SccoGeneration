import configparser
import csv
import json
import os
import pika
import requests
import sys

from tools.dict_occurrence import DictOccurrenceManager

config = configparser.ConfigParser()
config.read("config.ini")
input_csv_prefix = config["Paths"]["input_csv_prefix"]
rabbit_address = config["Rabbit"]["rabbit_address"]
in_queue = config["Rabbit"]["in_queue"]
out_queue = config["Rabbit"]["out_queue"]


def add_to_database(dict_database):
    pass  # TODO: implement


def on_message_received(ch, method, properties, body):
    print(f" [x] Received {body}")

    json_in = json.loads(body.decode())
    customer_id = json_in['customer_id']
    csv_url = json_in['parsed_csv']

    r = requests.get(csv_url)
    data = r.text.split('\n')
    data.pop(0)  # drop header

    words_black_list = {'Вакансия'}  # TODO get by customer_id
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


def send_message(channel, body):
    channel.basic_publish(exchange="", routing_key=out_queue, body=body)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(rabbit_address))
    channel = connection.channel()

    channel.queue_declare(queue=in_queue)
    channel.queue_declare(queue=out_queue)

    channel.basic_consume(
        queue=in_queue, auto_ack=True, on_message_callback=on_message_received
    )  # TODO: ack

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
