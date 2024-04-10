import inspect

from sqlalchemy import select
from sqlalchemy.orm import Session

from util.json_handle import dict_get_or_panic
import crud.dbapi as dbapi

# TODO: replace with ClientCRUD
from crud.models import Customer

import json

import db_functional_service.rmq_handle as rmq


def get_black_lists(query_data, reply, db_query):

    # Check keys.
    required_keys = [
        "customer_id",
    ]

    customer_ids = list()

    for row in query_data:
        for key in required_keys:
            customer_ids.append(dict_get_or_panic(row, key, db_query))

    # Make db query.
    print("Start query")
    engine = dbapi.DbEngine.get_engine()
    with Session(engine) as session:
        stmt = (select(Customer.customer_id, Customer.black_list)
                .where(Customer.customer_id.in_(customer_ids)))
        print("Make scalars")

        # Make query.
        db_answer = session.execute(stmt)

        # Validate columns.
        required_columns = ["customer_id", "black_list"]
        customer_id_ind = -1
        black_list_ind = -1
        for ind, column_name in enumerate(db_answer.keys()):
            if column_name == "customer_id":
                customer_id_ind = ind
            elif column_name == "black_list":
                black_list_ind = ind

        if customer_id_ind == -1 or black_list_ind == -1:
            RuntimeError(inspect.cleandoc(f"""
            Unexpected columns in result: {db_answer.keys()}
            Expected columns: {required_columns}"""))

        # Prepare answer.
        answer = []
        for row in db_answer:
            answer.append({
                "customer_id": row[customer_id_ind],
                "black_list": row[black_list_ind],
            })
    print("Finish query")

    # Send query to rabbitmq.
    answer = json.dumps(answer, indent=2)
    print(f"Answer:\n{answer}")
    rmq.RmqHandle.basic_publish(answer, reply)
