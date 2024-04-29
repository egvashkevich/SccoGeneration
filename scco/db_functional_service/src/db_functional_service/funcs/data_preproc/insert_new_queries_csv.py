import json

from util.json_handle import dict_get_or_panic
from util.reply_ctx import add_reply_ctx

from crud.objects.new_queries_csv import NewQueriesCsvCRUD

from db_functional_service.reply import Reply
from db_functional_service.broker.broker import Broker


def insert_new_queries_csv(
        req_data,
        srv_req_data,
        reply: Reply,
        broker: Broker
) -> None:
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

    print("Preparing answer")
    answer = {
        "csv_path": data_dict["csv_path"],
    }

    # Add reply_ctx.
    add_reply_ctx(srv_req_data, answer)

    # Send query to rabbitmq.
    answer = json.dumps(answer, indent=2)
    print(f"Answer:\n{answer}")

    print("sending reply")
    broker.basic_publish_unknown(
        reply.get_publisher(),
        answer.encode("utf-8"),
    )

