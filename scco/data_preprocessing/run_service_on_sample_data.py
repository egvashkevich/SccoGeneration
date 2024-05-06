#!/usr/bin/env python
import json
import os
import pika
import sys

import config

# Make sure config.RABBIT_ADDRESS is 'localhost' and rabbit is running


def main():
    # Send message
    connection = pika.BlockingConnection(pika.ConnectionParameters(config.RABBIT_ADDRESS))
    channel = connection.channel()

    channel.queue_declare(queue=config.IN_QUEUE, durable=True)

    message = json.dumps({
        'customer_id': '0',
        'parsed_csv': 'file://' + os.path.join(os.getcwd(), 'resources/sample_input.csv')
    })
    # in docker: {"customer_id": "0", "parsed_csv": "file:///data_preprocessing/resources/sample_input.csv"}
    # {"customer_id": "0", "parsed_csv": "file:///data_preprocessing/resources/test_data/it/all_freelance/Messages_Request_From_2024_04_29 (3).csv"}
    # {"customer_id": "0", "parsed_csv": "file:///data/new_queries/Messages_Request_From_2024_04_29 (3).csv"}

    channel.basic_publish(exchange="", routing_key=config.IN_QUEUE, body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=pika.DeliveryMode.Persistent
                          ))
    print(f" [x] Sent {message}")

    connection.close()

    # Receive message
    connection = pika.BlockingConnection(pika.ConnectionParameters(config.RABBIT_ADDRESS))
    channel = connection.channel()

    channel.queue_declare(queue=config.OUT_QUEUE, durable=True)

    def callback(ch, method, properties, body):
        body_readable = str(json.loads(body.decode()))
        print(f" [x] Received {body_readable}")

    channel.basic_consume(queue=config.OUT_QUEUE, auto_ack=True, on_message_callback=callback)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
