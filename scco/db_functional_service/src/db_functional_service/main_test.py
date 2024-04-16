import sys
import json

import db_functional_service.data.init_db
from util.json_handle import dict_get_or_panic

import crud.dbapi as dbapi
from crud.models import Base

import db_functional_service.rmq_handle as rmq
from db_functional_service.rmq_handle import Reply

# from db_functional_service.funcs.contains_queries import contains_queries
# from db_functional_service.funcs.get_black_lists import get_black_lists
# from db_functional_service.funcs.insert_preprocessed_queries import (
#     insert_preprocessed_queries
# )
# from db_functional_service.funcs.insert_offers import insert_offers
# from db_functional_service.funcs.ml_get_messages import ml_get_messages

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

# Requests.

from db_functional_service.data.data_preproc.filter_new_queries import (
    request_1 as fnq_request_1,
)
from db_functional_service.data.data_preproc.insert_new_queries_csv import (
    request_1 as inq_csv_request_1,
)
from db_functional_service.data.data_preproc.get_customers_black_lists import (
    request_1 as gcbl_request_1,
)
from db_functional_service.data.data_preproc.insert_preprocessed_queries import (
    request_1 as ipc_request_1,
)
from db_functional_service.data.pdf_co_gen.insert_offers import (
    request_1 as io_request_1,
)
from db_functional_service.data.ml_co_gen.get_info_for_co_generation import (
    request_1 as gifcog_request_1,
)
from db_functional_service.data.customer_creator.insert_customer import (
    request_1 as ic_request_1,
)

################################################################################
from db_functional_service.data.init_db import init_db


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

    init_db()


def main():
    init_database()

    # dispatch(fnq_request_1)
    # dispatch(inq_csv_request_1)
    # dispatch(gcbl_request_1)
    # dispatch(ipc_request_1)
    # dispatch(io_request_1)
    # dispatch(gifcog_request_1)
    dispatch(ic_request_1)
    # dispatch(io_request_1)

    # rmq.RmqHandle.setup_rmq(gateway_callback)
    # rmq.RmqHandle.start_consume()  # Infinite loop.


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted', file=sys.stderr)
    except Exception as e:
        print(f'Internal service unexpected error: {e}', file=sys.stderr)
        sys.exit(2)


################################################################################


# def text_query():
#     textual_sql = text(
#         "SELECT id, name, fullname FROM user_account ORDER BY id"
#         )
#     textual_sql = textual_sql.columns(User.id, User.name, User.fullname)
#     orm_sql = select(User).from_statement(textual_sql)
#     for user_obj in session.execute(orm_sql).scalars():
#         print(user_obj)
