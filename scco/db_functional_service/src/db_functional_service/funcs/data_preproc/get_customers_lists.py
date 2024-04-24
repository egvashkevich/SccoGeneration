from util.json_handle import dict_get_or_panic
import util.parse_env as ps
from util.reply_ctx import add_reply_ctx

import crud.dbapi as dbapi
from crud.models import Customer
from crud.objects.customer import CustomerCRUD

import json

import db_functional_service.rmq_handle as rmq


def get_customers_lists(req_data, reply, srv_req_data):
    print("Enter get_customers_lists")

    # Check keys.
    required_keys = [
        "customer_id",
    ]

    customer_ids = []

    for row in req_data:
        for key in required_keys:
            customer_ids.append(dict_get_or_panic(row, key, srv_req_data))

    # Make db query.
    print("Start query")
    engine = dbapi.DbEngine.get_engine()
    result_set = CustomerCRUD.select_all(
        [
            Customer.customer_id,
            Customer.black_list,
            Customer.white_list,
        ],
        wheres_cond=[
            Customer.customer_id.in_(customer_ids),
        ],
    )

    print("Collecting data")
    answer_list = []
    for row in result_set:
        answer_list.append(
            {
                "customer_id": row[0],
                "black_list": row[1],
                "white_list": row[2],
            }
        )

    print("Sending answer")
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
