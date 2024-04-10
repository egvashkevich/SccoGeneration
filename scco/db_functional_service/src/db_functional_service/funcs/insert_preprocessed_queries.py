import inspect

from util.json_handle import dict_get_or_panic
import crud.message_group_id_generator as mgig

from crud.objects.query import QueryCRUD
from crud.objects.client import ClientCRUD

import json


def flatten_query_dict(query_dict: dict) -> list[dict]:
    res = []
    for msg, date in zip(query_dict["messages"], query_dict["message_dates"]):
        res_item = {}
        for k, v in query_dict.items():
            if k == "messages":
                res_item["message"] = msg
            elif k == "message_dates":
                res_item["message_date"] = date
            else:
                res_item[k] = v
        res.append(res_item)

    return res


def insert_preprocessed_queries(query_data, reply, db_query):
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
        group_ids.append(group_id)

        insert_dicts = flatten_query_dict(data_dict)
        for query_dict in insert_dicts:
            query_dict["message_group_id"] = group_id

        # Insert new clients.
        for query_dict in insert_dicts:
            if not ClientCRUD.contain(query_dict["client_id"]):
                ClientCRUD.insert_one({
                    "client_id": query_dict["client_id"],
                    "attitude": "default"
                })

        # Insert queries.
        QueryCRUD.insert_all(insert_dicts)

    # Send query to rabbitmq.
    answer = json.dumps(group_ids, indent=2)
    print(f"Answer:\n{answer}")
    # ...
