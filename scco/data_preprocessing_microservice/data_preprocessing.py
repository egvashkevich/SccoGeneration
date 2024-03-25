import configparser
import pika
import sys
import os

config = configparser.ConfigParser()
config.read('config.ini')
rabbit_address = config["Rabbit"]["rabbit_address"]
in_queue = config["Rabbit"]["in_queue"]
out_queue = config["Rabbit"]["out_queue"]


def on_message_received(ch, method, properties, body):
    print(f" [x] Received {body}")

    # TODO: implement

    print(" [x] Done")


def send_message(channel, body):
    channel.basic_publish(exchange="", routing_key=out_queue, body=body)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_address))
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
