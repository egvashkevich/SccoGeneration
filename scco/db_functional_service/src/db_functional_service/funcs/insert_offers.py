import inspect

from sqlalchemy import select
from sqlalchemy import func as sqlfunc
from sqlalchemy import desc

from sqlalchemy.orm import Session

import crud.dbapi as dbapi

from crud.objects.offer import OfferCRUD

# TODO: replace with QueryCRUD
from crud.models import Query

from util.json_handle import dict_get_or_panic
import crud.message_group_id_generator as mgig

import json

import db_functional_service.rmq_handle as rmq


def insert_offers(query_data, reply, db_query):
    required_keys = [
        "message_group_id",
        "file",
    ]

    answer = []

    for row in query_data:
        # Validate keys.
        data_dict = {}
        for key in required_keys:
            data_dict[key] = dict_get_or_panic(row, key, db_query)

        # Get last query_id in message group, client_id, customer_id.
        engine = dbapi.DbEngine.get_engine()
        with Session(engine) as session:
            print("Enter insert_offers")
            stmt = (select(Query.query_id, Query.customer_id, Query.client_id)
                    .select_from(Query)
                    .where(
                Query.message_group_id == data_dict["message_group_id"]
            )
                    .order_by(desc(Query.message_date))
                    .limit(1))
            result_set = session.execute(stmt).one_or_none()
            if result_set is None:
                RuntimeError(inspect.cleandoc(f"""
                Unexpected error: no such message_group_id in table.
                message_group_id: {data_dict["message_group_id"]}
                query_data: {json.dumps(query_data, indent=2)}
                db_query: {json.dumps(db_query, indent=2)}"""))
            print(f"-----------------------------")
            print(f"result_set = {result_set}")
            print(f"-----------------------------")

            query_id = result_set[0]
            customer_id = result_set[1]
            client_id = result_set[2]

        # Get last query_id in message group.
        OfferCRUD.insert_one(
            {
                "query_id": query_id,
                "file": data_dict["file"],
            }
        )

        answer.append({
            "customer_id": customer_id,
            "client_id": client_id,
            "file": data_dict["file"],
        })

    # Send query to rabbitmq.
    answer = json.dumps(answer, indent=2)
    print(f"Answer:\n{answer}")
    rmq.RmqHandle.basic_publish(answer, reply)

    #     # Insert new clients.
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
