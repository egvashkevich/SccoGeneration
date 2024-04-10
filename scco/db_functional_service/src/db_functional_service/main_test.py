import sys

from util.json_handle import dict_get_or_panic

import crud.dbapi as dbapi

from crud.models import Base

import json

from db_functional_service.funcs.contains_queries import contains_queries
from db_functional_service.funcs.get_black_lists import get_black_lists
from db_functional_service.funcs.insert_preprocessed_queries import (
    insert_preprocessed_queries
)
from db_functional_service.funcs.insert_offers import insert_offers
from db_functional_service.funcs.ml_get_messages import ml_get_messages

# Dummy values.
from db_functional_service.data.init_db import init_db
from db_functional_service.data.insert_preprocessed_queries_data import (
    insert_preprocessed_queries_request_1
)
from db_functional_service.data.insert_offers_data import (
    insert_offers_request_1
)
from db_functional_service.data.insert_offers_data import (
    insert_offers_request_1
)
from db_functional_service.data.ml_get_messages_data import (
    ml_get_messages_request_1
)


class Reply:
    def __init__(self, db_query: dict):
        reply = dict_get_or_panic(db_query, "reply", db_query)
        self.exchange = dict_get_or_panic(reply, "exchange", db_query)
        self.queue = dict_get_or_panic(reply, "queue", db_query)
        self.routing_key = dict_get_or_panic(reply, "routing_key", db_query)


def get_query_data(db_query):
    if "query_data" in db_query:
        return db_query["query_data"]
    else:
        raise RuntimeError(
            f"No query_data provided. Query content: '{db_query}'"
        )


def gateway_callback(ch, method, properties, body):
    json_query = body.decode("utf-8")
    json_query = json.loads(json_query)
    dispatch(json_query)


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


# def text_query():
#     textual_sql = text(
#         "SELECT id, name, fullname FROM user_account ORDER BY id"
#         )
#     textual_sql = textual_sql.columns(User.id, User.name, User.fullname)
#     orm_sql = select(User).from_statement(textual_sql)
#     for user_obj in session.execute(orm_sql).scalars():
#         print(user_obj)


def main():
    print("Creating db engine")
    engine = dbapi.DbEngine.get_engine()
    print("Db engine created")

    # Create tables.
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    init_db(engine)

    # dispatch(contains_query_request_1)
    # dispatch(get_black_list_request_1)
    # dispatch(insert_preprocessed_queries_request_1)
    # dispatch(insert_offers_request_1)
    dispatch(ml_get_messages_request_1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted', file=sys.stderr)
    except Exception as e:
        print(f'Unexpected error: {e}', file=sys.stderr)
        sys.exit(2)

    # util.print_env_variables(env_config)

    # users = session.scalars(
    #     insert(User).returning(User),
    #     [
    #         {"name": "spongebob", "fullname": "Spongebob Squarepants"},
    #         {"name": "sandy", "fullname": "Sandy Cheeks"},
    #     ],
    # )
    # print(users.all())


################################################################################
