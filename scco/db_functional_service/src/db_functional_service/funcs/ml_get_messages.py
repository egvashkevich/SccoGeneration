import inspect

from sqlalchemy import select
from sqlalchemy import func as sqlfunc
from sqlalchemy import desc

from sqlalchemy.orm import Session
import crud.dbapi as dbapi

from crud.models import Query

from util.json_handle import dict_get_or_panic
import crud.message_group_id_generator as mgig

import json

import db_functional_service.rmq_handle as rmq


def ml_get_messages(query_data, reply, db_query):
    required_keys = [
        "message_group_id",
    ]

    # Validate keys.
    data_dict = {}
    for key in required_keys:
        data_dict[key] = dict_get_or_panic(query_data, key, db_query)

    # Make Query.
    engine = dbapi.DbEngine.get_engine()
    with Session(engine) as session:
        print("Enter ml_get_messages")
        stmt = (select(Query.customer_id,
                       Query.client_id,
                       Query.message,
                       Query.message_date)
                .select_from(Query)
                .where(
            Query.message_group_id == data_dict["message_group_id"]
        )
                .order_by(desc(Query.message_date)))
        result_set = session.execute(stmt).all()
        if result_set is None:
            RuntimeError(inspect.cleandoc(f"""
            Unexpected error: no such message_group_id in table.
            message_group_id: {data_dict["message_group_id"]}
            query_data: {json.dumps(query_data, indent=2)}
            db_query: {json.dumps(db_query, indent=2)}"""))
        print(f"-----------------------------")
        print(f"result_set = {result_set}")
        print(f"-----------------------------")

        customer_id = result_set[0][0]
        client_id = result_set[0][1]
        messages = []
        for row in result_set:
            messages.append(row[2])

        answer = {
            "customer_id": customer_id,
            "client_id": client_id,
            "messages": messages,
            "history": []
        }

        # Send query to rabbitmq.
        answer = json.dumps(answer, indent=2)
        print(f"Answer:\n{answer}")
        rmq.RmqHandle.basic_publish(answer, reply)
