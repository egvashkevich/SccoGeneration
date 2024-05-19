import utils.app_config as app_cfg

import inspect
import json

from broker_for_creator.Broker import Broker
from broker_for_creator.Broker import Publisher
from broker_for_creator.Broker import Consumer

def get_callback_data(body: bytes):
    body = body.decode("utf-8")
    print_request_body(body)
    res = json.loads(body)
    return res


def publish_answer(
        answer,
        publisher_name: str,
        broker: Broker,
) -> None:
    # Send query to rabbitmq.
    answer = json.dumps(answer, indent=2, ensure_ascii=False)
    print(f"Answer:\n{answer}")

    print("sending answer")
    broker.basic_publish(
        publisher_name,
        answer.encode("utf-8"),
    )


def print_request_body(body) -> None:
    print(
        f"""
body of request:
-----------
{body}
----------"""
    )


class InsertToDb:
    # Publishers
    customer_creator_pub = "customer_creator_pub"

    def __init__(self, broker: Broker):
        self.broker = broker

        broker.add_consumer(
            Consumer(
                exchange=app_cfg.CUSTOMER_CREATOR_EXCHANGE,
                queue=app_cfg.CUSTOMER_CREATOR_QUEUE,
                routing_key=app_cfg.CUSTOMER_CREATOR_ROUTING_KEY,
                callback=self.callback,
            )
        )
        broker.add_publisher(
            Publisher(
                name=InsertToDb.customer_creator_pub,
                exchange=app_cfg.DB_FUNCTIONAL_SERVICE_EXCHANGE,
                queue=app_cfg.DB_FUNCTIONAL_SERVICE_QUEUE,
                routing_key=app_cfg.DB_FUNCTIONAL_SERVICE_ROUTING_KEY,
            )
        )

    def callback(self, ch, method, props, body):
        print("InsertToDb callback started")
        passed_data = get_callback_data(body)

        answer = self.callback_handle(passed_data)

        publish_answer(answer, self.customer_creator_pub, self.broker)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("InsertToDb callback finished")

    def callback_handle(self, passed_data) -> dict:
        # Создаем копию passed_data и добавляем white_list
        request_data = passed_data.copy()
        request_data["white_list"] = passed_data["tags"]
    
        # Формируем итоговый словарь, добавляя ключи в нужном порядке
        answer = {
            "request_name": "insert_customer",
            "request_data": {
                "customer_id": request_data["customer_id"],
                "contact_info": request_data["contact_info"],
                "company_name": request_data["company_name"],
                "black_list": request_data["black_list"],
                "tags": request_data["tags"],
                "white_list": request_data["white_list"],
                "specific_features": request_data["specific_features"],
                "services": request_data["services"]
            }
        }
        return answer
