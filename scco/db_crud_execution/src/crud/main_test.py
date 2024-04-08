import sys

from util import json_get_or_panic

import dbapi

from models import Base

import json

from queries.contains_query import contains_query
from queries.get_black_list import get_black_list
from queries.insert_preprocessed_queries import insert_preprocessed_queries

# Dummy values.
from crud.queries.templates.db_init_dummy_values import db_init_dummy_values
from crud.queries.templates.contains_query_t import contains_query_request_1
from crud.queries.templates.get_black_list_t import get_black_list_request_1
from crud.queries.templates.insert_preprocessed_queries import (
    insert_preprocessed_queries_request_1
)


class Reply:
    def __init__(self, db_query: dict):
        reply = json_get_or_panic(db_query, "reply", db_query)
        self.exchange = json_get_or_panic(reply, "exchange", db_query)
        self.queue = json_get_or_panic(reply, "queue", db_query)
        self.routing_key = json_get_or_panic(reply, "routing_key", db_query)


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
    query_data = json_get_or_panic(db_query, "query_data", db_query)
    reply = Reply(db_query)

    print("Start dispatch")

    query_name = db_query["query_name"]
    if query_name == "contains_query":
        contains_query(query_data, reply, db_query)
    elif query_name == "get_black_list":
        get_black_list(query_data, reply, db_query)
    elif query_name == "insert_preprocessed_queries":
        insert_preprocessed_queries(query_data, reply, db_query)
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

    db_init_dummy_values(engine)

    # dispatch(contains_query_request_1)
    # dispatch(get_black_list_request_1)
    dispatch(insert_preprocessed_queries_request_1)


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
