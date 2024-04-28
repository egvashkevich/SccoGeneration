import json

import util.app_config as app_cfg

from ml_generation.broker.broker import Broker
from ml_generation.broker.broker import Publisher
from ml_generation.broker.broker import Consumer


class Preproc:
    def __init__(self, broker: Broker):
        self.broker = broker

        # Publishers.
        self.db_service = "preproc_step.db_service"

        broker.add_consumer(
            Consumer(
                exchange=app_cfg.ML_GENERATION_EXCHANGE,
                queue=app_cfg.ML_GENERATION_QUEUE,
                routing_key=app_cfg.ML_GENERATION_ROUTING_KEY,
                callback=self.callback,
            )
        )
        broker.add_publisher(
            Publisher(
                name=self.db_service,
                exchange=app_cfg.DB_FUNCTIONAL_SERVICE_EXCHANGE,
                queue=app_cfg.DB_FUNCTIONAL_SERVICE_QUEUE,
                routing_key=app_cfg.DB_FUNCTIONAL_SERVICE_ROUTING_KEY,
            )
        )

    def callback(self, ch, method, props, body):
        print("Preproc callback started")

        # Get data from body.
        body = body.decode("utf-8")
        print(
            f"""body from preprocessed_data:
            -----------
            {body}
            ----------"""
        )
        passed_data = json.loads(body)

        message_group_id = passed_data["message_group_id"]

        request = {
            "request_name": "get_info_for_co_generation",
            "reply": {
                "exchange": app_cfg.CO_GEN_EXCHANGE,
                "routing_key": app_cfg.CO_GEN_ROUTING_KEY,
            },
            "reply_ctx": message_group_id,  # not required
            "request_data": {
                "message_group_id": message_group_id,
            }
        }
        request = json.dumps(request)
        body = request.encode("utf-8")
        self.broker.basic_publish(self.db_service, body)

        ch.basic_ack(delivery_tag=method.delivery_tag)

        print("Preproc callback finished")
