import inspect
import json
import base64

import util.app_config as app_cfg

from ml_generation.broker.broker import Broker
from ml_generation.broker.broker import Publisher
from ml_generation.broker.broker import Consumer

from ml_models.co_gen.api import GenerateGateWrapper as CoMlModel


class CoGen:
    # Publishers
    pdf_generation_pub = "co_gen.pdf_gen"

    def __init__(self, broker: Broker, ml_model):
        self.broker = broker
        self.ml_model = ml_model

        broker.add_consumer(
            Consumer(
                exchange=app_cfg.CO_GEN_EXCHANGE,
                queue=app_cfg.CO_GEN_QUEUE,
                routing_key=app_cfg.CO_GEN_ROUTING_KEY,
                callback=self.callback,
            )
        )
        broker.add_publisher(
            Publisher(
                name=CoGen.pdf_generation_pub,
                exchange=app_cfg.PDF_GENERATION_EXCHANGE,
                queue=app_cfg.PDF_GENERATION_QUEUE,
                routing_key=app_cfg.PDF_GENERATION_ROUTING_KEY,
            )
        )

    def callback(self, ch, method, props, body):
        print("CoGen callback started")

        # Get data from body.
        body = body.decode("utf-8")
        print(
            inspect.cleandoc(
                f"""body from db_functional_service:
-----------
{body}
----------"""
            )
        )
        print("converting json to python objects (json.loads())")
        passed_data = json.loads(body)
        message_group_id = passed_data["reply_ctx"]

        # Run model.
        # TODO: replace when ready
        print("Running model.generate_offer_text()...")
        gen_data = self.ml_model.generate_offer_text(passed_data)
        # ml_not_ready = True
        # if ml_not_ready:
        #     gen_data = {
        #         "main_text": "some_useful_text"
        #     }
        # else:
        #     gen_data = self.ml_model.generate_offer_text(passed_data)

        print(f"model.generate_offer_text() finished, gen_data:\n{gen_data}")

        main_text = gen_data["main_text"]
        main_text_bytes = main_text.encode('utf-8')
        main_text_b64_bytes = base64.b64encode(main_text_bytes)
        main_text_b64_string = main_text_b64_bytes.decode('utf-8')

        answer = {
            "message_group_id": message_group_id,
            "main_text": main_text_b64_string,
        }
        request = json.dumps(answer)
        body = request.encode("utf-8")
        print(f"Sending body:\n----------\n{body}\n-----------")
        self.broker.basic_publish(self.pdf_generation_pub, body)

        ch.basic_ack(delivery_tag=method.delivery_tag)

        print("CoGen callback finished")
