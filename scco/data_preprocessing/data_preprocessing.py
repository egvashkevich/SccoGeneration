import configparser
import csv
import pika
import sys
import os

from tools.dict_occurrence import DictOccurrenceManager

config = configparser.ConfigParser()
config.read("config.ini")
input_csv_prefix = config["Paths"]["input_csv_prefix"]
rabbit_address = config["Rabbit"]["rabbit_address"]
in_queue = config["Rabbit"]["in_queue"]
out_queue = config["Rabbit"]["out_queue"]


def add_to_database(row):
    pass  # TODO: implement


def on_message_received(ch, method, properties, body):
    print(f" [x] Received {body}")

    path_to_csv = input_csv_prefix + body.decode()
    with open(path_to_csv) as csvfile:
        data = csvfile.readlines()
    data.pop(0)  # drop header

    words_black_list = {'Вакансия'}  # TODO get by user id
    occurrenceManager = DictOccurrenceManager(words_black_list)

    csv_reader = csv.reader(data)
    for row_raw, row_list in zip(data, csv_reader):  # can we make it async?
        client_message = row_list[2]
        if occurrenceManager.check_occurrence_with_errors(client_message, 2):
            continue  # ignore this client
        # TODO: check if already in database
        add_to_database(row_list)
        send_message(ch, row_raw)

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
