from crud.objects.new_queries_csv import NewQueriesCsvCRUD

from util.json_handle import dict_get_or_panic

import json

import db_functional_service.rmq_handle as rmq

import util.parse_env as ps

from util.reply_ctx import add_reply_ctx


def insert_new_queries_csv(req_data, reply, srv_req_data):
    print("Enter get_customers_black_lists")

    # Check keys.
    required_keys = [
        "csv_path",
    ]

    data_dict = {}
    for key in required_keys:
        data_dict[key] = dict_get_or_panic(req_data, key, srv_req_data)

    # Make db query.
    print("Start query")
    NewQueriesCsvCRUD.insert_one(
        {
            "csv_path": data_dict["csv_path"],
        }
    )
    print("Finish query")

    answer = {
        "csv_path": data_dict["csv_path"],
    }

    # Add reply_ctx.
    add_reply_ctx(srv_req_data, answer)

    # Send query to rabbitmq.
    answer = json.dumps(answer, indent=2)
    print(f"Answer:\n{answer}")

    if not ps.is_on_host():
        rmq.RmqHandle.basic_publish(answer, reply)
