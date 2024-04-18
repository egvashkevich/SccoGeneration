import json

import ml_generation.broker_config as bc

from ml_generation.rmq_broker import RmqBroker
from ml_generation.rmq_broker import Publisher
from ml_generation.rmq_broker import Consumer

from ml_generation.steps.wrap_step import wrap_step_callback

from ml_models.co_gen.api import GenerateGateWrapper as CoMlModel


class CoGen:
    def __init__(self, broker: RmqBroker):
        self.broker = broker

        # Publishers.
        self.pdf_gen = "gen_step.pdf_gen"

        broker.add_consumer(
            Consumer(
                exchange=bc.CO_GEN_EXCHANGE,
                queue=bc.CO_GEN_QUEUE,
                routing_key=bc.CO_GEN_ROUTING_KEY,
                callback=self.callback,
            )
        )
        broker.add_publisher(
            Publisher(
                name="gen_step.pdf_gen",
                exchange=bc.PDF_GENERATION_EXCHANGE,
                queue=bc.PDF_GENERATION_QUEUE,
                routing_key=bc.PDF_GENERATION_ROUTING_KEY,
            )
        )

    def callback(self, ch, method, props, body):
        print("CoGen callback started")

        # Get data from body.
        body = body.decode("utf-8")
        print(
            f"""body from db_functional_service:
            -----------
            {body}
            ----------"""
        )
        print("converting json to python objects (json.loads())")
        passed_data = json.loads(body)
        message_group_id = passed_data["reply_ctx"]

        # Run model.
        # TODO: replace when ready
        print("Running model.generate_offer_text()...")
        ml_not_ready = True
        if ml_not_ready:
            gen_data = {
                "main_text": "some_useful_text"
            }
        else:
            model = CoMlModel()
            gen_data = model.generate_offer_text(passed_data)

        print(f"model.generate_offer_text() finished, gen_data:\n{gen_data}")

        main_text = gen_data["main_text"]

        answer = {
            "message_group_id": message_group_id,
            "main_text": main_text,
        }
        request = json.dumps(answer)
        body = request.encode("utf-8")
        print(f"Sending body:\n----------{body}\n-----------")
        self.broker.basic_publish(self.pdf_gen, body)

        print("CoGen callback finished")
