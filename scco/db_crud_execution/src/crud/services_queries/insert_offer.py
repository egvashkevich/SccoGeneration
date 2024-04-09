import inspect

from sqlalchemy import insert
from sqlalchemy.orm import Session

from crud.dao.query_dao import QueryDAO
from crud.models import Query
from crud.json_util import dict_get_or_panic
import crud.dbapi as dbapi
import crud.message_group_id_generator as mgig

from crud.dao.client_dao import ClientDAO

import json


def insert_offer(query_data, reply, db_query):
    required_keys = [
        "customer_id",
        "client_id",
        "channel_id",
        "messages",
        "message_dates",
    ]

    group_ids = []

    for row in query_data:
        # Validate keys.
        data_dict = {}
        for key in required_keys:
            data_dict[key] = dict_get_or_panic(row, key, db_query)
        if len(data_dict["messages"]) != len(data_dict["message_dates"]):
            RuntimeError(
                inspect.cleandoc(
                    f"""
                Length of messages and message_dates do not match.
                ---------------------------------
                row = {json.dumps(row, indent=2)}
                ---------------------------------
                db_query = {json.dumps(db_query, indent=2)}
                """
                )
            )

        # Prepare data for insertion.
        group_id = mgig.IdGenerator.reserve_id()
        print("--------------------------")
        print(group_id)
        print("--------------------------")
        group_ids.append(group_id)

        insert_dicts = flatten_query_dict(data_dict)
        for query_dict in insert_dicts:
            query_dict["message_group_id"] = group_id

        # Insert new clients.
        for query_dict in insert_dicts:
            if not ClientDAO.contain(query_dict["client_id"]):
                ClientDAO.insert_one({
                    "client_id": query_dict["client_id"],
                    "attitude": "default"
                })

        # Insert queries.
        QueryDAO.insert_all(insert_dicts)

    # Send query to rabbitmq.
    answer = json.dumps(group_ids, indent=2)
    print(f"Answer:\n{answer}")
    # ...
