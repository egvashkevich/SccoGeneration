import inspect

from sqlalchemy import select
from sqlalchemy import func as sqlfunc
from sqlalchemy import desc

from sqlalchemy.orm import Session

import crud.dbapi as dbapi

from crud.objects.offer import OfferCRUD

# TODO: replace with QueryCRUD
from crud.models import Query
from crud.objects.query import QueryCRUD

from util.json_handle import dict_get_or_panic
import crud.message_group_id_generator as mgig

import json

import db_functional_service.rmq_handle as rmq

import util.parse_env as ps

from util.reply_ctx import add_reply_ctx


# Updates data_dict. Inserts:
# - query_id
# - customer_id
# - client_id
def select_from_query(data_dict, req_data, srv_req_data) -> None:
    result_set = QueryCRUD.select_one(
        [Query.query_id, Query.customer_id, Query.client_id],
        wheres_cond=[
            Query.message_group_id == data_dict["message_group_id"]
        ],
        order_bys=[desc(Query.message_date)],
    )
    if result_set is None:
        RuntimeError(
            inspect.cleandoc(
                f"""
        Unexpected error: no such message_group_id in table.
        message_group_id: {data_dict["message_group_id"]}
        req_data: {json.dumps(req_data, indent=2)}
        srv_req_data: {json.dumps(srv_req_data, indent=2)}"""
            )
        )
    print(f"-----------------------------")
    print(f"result_set = {result_set}")
    print(f"-----------------------------")

    res = {
        "query_id": result_set[0],
        "customer_id": result_set[1],
        "client_id": result_set[2],
    }

    data_dict.update(res)


def insert_offers(req_data, reply, srv_req_data):
    print("Enter insert_offers")

    required_keys = [
        "message_group_id",
        "file_path",
    ]

    answer_list = []

    for row in req_data:
        # Validate keys.
        data_dict = {}
        for key in required_keys:
            data_dict[key] = dict_get_or_panic(row, key, srv_req_data)

        select_from_query(data_dict, req_data, srv_req_data)

        # Hook file to the most recent message in the message group.
        OfferCRUD.insert_one(
            {
                "query_id": data_dict["query_id"],
                "file_path": data_dict["file_path"],
            }
        )

        answer_list.append({
            "customer_id": data_dict["customer_id"],
            "client_id": data_dict["client_id"],
            "file_path": data_dict["file_path"],
        })

    answer = {
        "array_data": answer_list,
    }

    # Add reply_ctx.
    add_reply_ctx(srv_req_data, answer)

    # Send query to rabbitmq.
    answer = json.dumps(answer, indent=2)
    print(f"Answer:\n{answer}")

    if not ps.is_on_host():
        rmq.RmqHandle.basic_publish(answer, reply)

    #     # Insert new customer.
    #     for query_dict in insert_dicts:
    #         if not ClientDAO.contain(query_dict["client_id"]):
    #             ClientDAO.insert_one({
    #                 "client_id": query_dict["client_id"],
    #                 "attitude": "default"
    #             })
    #
    #     # Insert queries.
    #     QueryDAO.insert_all(insert_dicts)
    #
    # # Send query to rabbitmq.
    # answer = json.dumps(group_ids, indent=2)
    # print(f"Answer:\n{answer}")
    # # ...
