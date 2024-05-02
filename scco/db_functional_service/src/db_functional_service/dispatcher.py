import json

from util.json_handle import dict_get_or_panic

from db_functional_service.rmq_handle import Reply

from db_functional_service.broker.broker import Broker
from db_functional_service.broker.broker import Consumer

import util.app_config as app_cfg

################################################################################

# Funcs

from db_functional_service.funcs.data_preproc.filter_new_queries import (
    filter_new_queries,
)
from db_functional_service.funcs.data_preproc.insert_new_queries_csv import (
    insert_new_queries_csv,
)
from db_functional_service.funcs.data_preproc.get_customers_lists import (
    get_customers_lists,
)
from db_functional_service.funcs.data_preproc.insert_preprocessed_queries import (
    insert_preprocessed_queries,
)
from db_functional_service.funcs.pdf_co_gen.insert_offers import (
    insert_offers,
)
from db_functional_service.funcs.ml_co_gen.get_info_for_co_generation import (
    get_info_for_co_generation,
)
from db_functional_service.funcs.customer_creator.insert_customer import (
    insert_customer,
)

################################################################################


class Dispatcher:
    def __init__(self, broker: Broker):
        self.broker = broker

        # Publishers.
        # ...

        broker.add_consumer(
            Consumer(
                exchange=app_cfg.DB_FUNCTIONAL_SERVICE_EXCHANGE,
                queue=app_cfg.DB_FUNCTIONAL_SERVICE_QUEUE,
                routing_key=app_cfg.DB_FUNCTIONAL_SERVICE_ROUTING_KEY,
                callback=self.callback,
            )
        )

    def callback(self, ch, method, props, body):
        print("Dispatcher callback started")

        # Get data from body.
        body = body.decode("utf-8")
        print(
            f"""body of request:
            -----------
            {body}
            ----------"""
        )
        print("converting json to python objects (json.loads())")
        srv_req_data = json.loads(body)

        self.dispatch_function(srv_req_data)

        ch.basic_ack(delivery_tag=method.delivery_tag)

        print("Dispatcher callback finished")

    def extract_req_data(self):
        pass

    def dispatch_function(self, srv_req_data):
        print("dispatch_function")

        req_data = dict_get_or_panic(srv_req_data, "request_data")
        reply = Reply(srv_req_data)

        query_name = dict_get_or_panic(srv_req_data, "request_name")
        if query_name == "filter_new_queries":
            filter_new_queries(req_data, srv_req_data, reply, self.broker)
        elif query_name == "insert_new_queries_csv":
            insert_new_queries_csv(req_data, srv_req_data, reply, self.broker)
        elif query_name == "get_customers_lists":
            get_customers_lists(req_data, srv_req_data, reply, self.broker)
        elif query_name == "insert_preprocessed_queries":
            insert_preprocessed_queries(req_data, srv_req_data,
                                        reply, self.broker)
        elif query_name == "insert_offers":
            insert_offers(req_data, srv_req_data, reply, self.broker)
        elif query_name == "get_info_for_co_generation":
            get_info_for_co_generation(req_data, srv_req_data,
                                       reply, self.broker)
        elif query_name == "insert_customer":
            insert_customer(req_data, srv_req_data, reply, self.broker)
        else:
            # TODO: print possible values
            raise RuntimeError(f"Unknown query_name: '{query_name}'")

