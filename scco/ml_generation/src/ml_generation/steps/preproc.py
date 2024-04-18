import json

import ml_generation.broker_config as bc

from ml_generation.rmq_broker import RmqBroker
from ml_generation.rmq_broker import Publisher
from ml_generation.rmq_broker import Consumer

from ml_generation.steps.wrap_step import wrap_step_callback


class Preproc:
    def __init__(self, broker: RmqBroker):
        self.broker = broker

        # Publishers.
        self.db_service = "preproc_step.db_service"

        broker.add_consumer(
            Consumer(
                exchange=bc.ML_GENERATION_EXCHANGE,
                queue=bc.ML_GENERATION_QUEUE,
                routing_key=bc.ML_GENERATION_ROUTING_KEY,
                callback=self.callback,
            )
        )
        broker.add_publisher(
            Publisher(
                name=self.db_service,
                exchange=bc.DB_FUNCTIONAL_SERVICE_EXCHANGE,
                queue=bc.DB_FUNCTIONAL_SERVICE_QUEUE,
                routing_key=bc.DB_FUNCTIONAL_SERVICE_ROUTING_KEY,
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
                "exchange": bc.CO_GEN_EXCHANGE,
                "routing_key": bc.CO_GEN_ROUTING_KEY,
            },
            "reply_ctx": message_group_id,  # not required
            "request_data": {
                "message_group_id": message_group_id,
            }
        }
        request = json.dumps(request)
        body = request.encode("utf-8")
        self.broker.basic_publish(self.db_service, body)

        print("Preproc callback finished")
