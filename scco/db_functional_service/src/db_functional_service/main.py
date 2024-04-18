import sys
import json

from util.json_handle import dict_get_or_panic

import crud.dbapi as dbapi
from crud.models import Base

import db_functional_service.rmq_handle as rmq
from db_functional_service.rmq_handle import Reply

################################################################################

# Funcs

from db_functional_service.funcs.data_preproc.filter_new_queries import (
    filter_new_queries,
)
from db_functional_service.funcs.data_preproc.insert_new_queries_csv import (
    insert_new_queries_csv,
)
from db_functional_service.funcs.data_preproc.get_customers_black_lists import (
    get_customers_black_lists,
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

from crud.objects.customer import CustomerCRUD
from crud.objects.customer_service import CustomerServiceCRUD

from db_functional_service.data.init_db import dummy_init_db


def gateway_callback(ch, method, properties, body):
    json_db_query = body.decode("utf-8")
    srv_req_data = json.loads(json_db_query)
    dispatch(srv_req_data)


def dispatch(srv_req_data):
    req_data = dict_get_or_panic(srv_req_data, "request_data", srv_req_data)
    reply = Reply(srv_req_data)

    print("Start dispatch")

    query_name = srv_req_data["request_name"]
    if query_name == "filter_new_queries":
        filter_new_queries(req_data, reply, srv_req_data)
    elif query_name == "insert_new_queries_csv":
        insert_new_queries_csv(req_data, reply, srv_req_data)
    elif query_name == "get_customers_black_lists":
        get_customers_black_lists(req_data, reply, srv_req_data)
    elif query_name == "insert_preprocessed_queries":
        insert_preprocessed_queries(req_data, reply, srv_req_data)
    elif query_name == "insert_offers":
        insert_offers(req_data, reply, srv_req_data)
    elif query_name == "get_info_for_co_generation":
        get_info_for_co_generation(req_data, reply, srv_req_data)
    elif query_name == "insert_customer":
        insert_customer(req_data, reply, srv_req_data)
    else:
        # TODO: print possible values
        raise RuntimeError(f"Unknown query_name: '{query_name}'")


def fake_init_db_data():
    dummy_init_db()

    # print("Start fake_init_db_data", flush=True)
    #
    # ############################################################################
    # # Customer.
    # customer_1 = {
    #     "customer_id": "customer_1",
    #     "contact_info": "telegram_link",
    #     "company_name": "Company of customer 1",
    #     "black_list": ["fuck", "shit", "nigger"],
    #     "tags": ["python", "b2b"],
    #     "white_list": ["python_synonym", "b2b_synonym"],
    #     "specific_features": ["feature_1", "feature_2"],
    # }
    # customer_2 = {
    #     "customer_id": "customer_2",
    #     "contact_info": "whatsapp_link",
    #     "company_name": "Company of customer 2",
    #     "black_list": ["bitch", "freak"],
    #     "tags": ["golang", "devops"],
    #     "white_list": ["golang_synonym", "devops_synonym"],
    #     "specific_features": ["feature_1", "feature_2"],
    # }
    # print("Start insert customers", flush=True)
    # CustomerCRUD.insert_all([customer_1, customer_2])
    # print("Finished insert customers", flush=True)
    #
    # ############################################################################
    # # CustomerService.
    # customer_services = [
    #     {
    #         "customer_id": "customer_1",
    #         "service_name": "customer 1, service 1",
    #         "service_desc": "description 1",
    #     },
    #     {
    #         "customer_id": "customer_1",
    #         "service_name": "customer 1, service 2",
    #         "service_desc": "description 2",
    #     },
    #     {
    #         "customer_id": "customer_2",
    #         "service_name": "customer 2, service 1",
    #         "service_desc": "description 1",
    #     }
    # ]
    # print("Start insert customer_services", flush=True)
    # CustomerServiceCRUD.insert_all(customer_services)
    # print("Finished insert customer_services", flush=True)
    #
    # print("Finish fake_init_db_data", flush=True)


def init_database():
    print("Creating db engine", flush=True)
    engine = dbapi.DbEngine.get_engine()
    print("Db engine created", flush=True)

    print("Removing old tables", flush=True)
    Base.metadata.drop_all(engine)
    print("Old tables removed", flush=True)

    print("Creating tables", flush=True)
    Base.metadata.create_all(engine)
    print("Tables created", flush=True)

    fake_init_db_data()


def main():
    init_database()

    print("Setup rmq", flush=True)
    rmq.RmqHandle.setup_rmq(gateway_callback)
    print("Start consuming", flush=True)
    rmq.RmqHandle.start_consume()  # Infinite loop.


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted', file=sys.stderr)
    except Exception as e:
        print(f'Internal service unexpected error: {e}', file=sys.stderr)
        sys.exit(2)
