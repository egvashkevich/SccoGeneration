import util.app_config as app_cfg

from broker_for_creator.broker import Broker
from broker_for_creator.broker import Publisher
from broker_for_creator.broker import Consumer

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
    insert_to_db_pub = "insert_to_db"

    def __init__(self, broker: Broker):
        self.broker = broker

        broker.add_consumer(
            Consumer(
                exchange=app_cfg.INSERT_TO_DB_EXCHANGE,# Добавить в конфиги
                queue=app_cfg.INSERT_TO_DB_QUEUE, # Добавить в конфиги
                routing_key=app_cfg.INSERT_TO_DB_ROUTING_KEY, # Добавить в конфиги
                callback=self.callback,
            )
        )
        broker.add_publisher(
            Publisher(
                name=INSERT_TO_DB.insert_to_db,
                exchange=app_cfg.INSERT_REQUEST_EXCHANGE, #Исправить 
                queue=app_cfg.INSERT_REQUEST_QUEUE, # Исправить
                routing_key=app_cfg.INSERT_REQUEST_ROUTING_KEY, # Исправить
            )
        )

    def callback(self, ch, method, props, body):
        print("InsertToDb callback started")
        passed_data = get_callback_data(body)

        answer = self.callback_handle(passed_data)

        publish_answer(answer, self.pdf_generation_pub, self.broker)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("InsertToDb callback finished")

    def callback_handle(self, passed_data) -> dict:
        transformed_data = {
    "request_name": "insert_customer",
    "request_data": passed_data
        }
        transformed_data["request_data"]["white_list"] = passed_data["tags"]
        answer = transformed_data
        return answer

