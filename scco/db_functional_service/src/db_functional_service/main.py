import sys
import json

from util.json_handle import dict_get_or_panic

import crud.dbapi as dbapi
from crud.models import Base

import db_functional_service.rmq_handle as rmq
from db_functional_service.rmq_handle import Reply

from db_functional_service.funcs.contains_queries import contains_queries
from db_functional_service.funcs.get_black_lists import get_black_lists
from db_functional_service.funcs.insert_preprocessed_queries import (
    insert_preprocessed_queries
)
from db_functional_service.funcs.insert_offers import insert_offers
from db_functional_service.funcs.ml_get_messages import ml_get_messages


def dispatch(db_query):
    query_data = dict_get_or_panic(db_query, "query_data", db_query)
    reply = Reply(db_query)

    print("Start dispatch")

    query_name = db_query["query_name"]
    if query_name == "contains_queries":
        contains_queries(query_data, reply, db_query)
    elif query_name == "get_black_lists":
        get_black_lists(query_data, reply, db_query)
    elif query_name == "insert_preprocessed_queries":
        insert_preprocessed_queries(query_data, reply, db_query)
    elif query_name == "insert_offers":
        insert_offers(query_data, reply, db_query)
    elif query_name == "ml_get_messages":
        ml_get_messages(query_data, reply, db_query)
    else:
        # TODO: print possible values
        raise RuntimeError(f"Unknown query_name: '{query_name}'")


def gateway_callback(ch, method, properties, body):
    json_db_query = body.decode("utf-8")
    db_query = json.loads(json_db_query)
    dispatch(db_query)


def init_database():
    print("Creating db engine", flush=True)
    engine = dbapi.DbEngine.get_engine()
    print("Db engine created", flush=True)

    print("Creating tables", flush=True)
    Base.metadata.create_all(engine)
    print("Tables created", flush=True)


def main():
    init_database()

    rmq.RmqHandle.setup_rmq(gateway_callback)
    rmq.RmqHandle.start_consume()  # Infinite loop.


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted', file=sys.stderr)
    except Exception as e:
        print(f'Service unexpected error: {e}', file=sys.stderr)
        sys.exit(2)
