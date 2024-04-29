import json

from util.json_handle import dict_has_or_panic
from util.reply_ctx import add_reply_ctx

from crud.models import Query
from crud.objects.query import QueryCRUD

from db_functional_service.reply import Reply
from db_functional_service.broker.broker import Broker


def filter_new_queries_predicate(row):
    print("Enter filter_new_queries_predicate")
    result_set = QueryCRUD.select_one(
        columns=[
            Query.client_id
        ],
        wheres_cond=[
            Query.customer_id == row["customer_id"],
            Query.client_id == row["client_id"],
            Query.channel_id == row["channel_id"],
            Query.message_date == row["message_date"]
        ]
    )
    res = (result_set is None)
    return res  # without raws


def filter_new_queries(
        req_data,
        srv_req_data,
        reply: Reply,
        broker: Broker
) -> None:
    print("Enter filter_new_queries")

    # Check keys.
    required_keys = [
        "customer_id",
        "client_id",
        "channel_id",
        "message_date",
    ]

    for row in req_data:
        for key in required_keys:
            dict_has_or_panic(row, key, srv_req_data)

    # Make db query.
    print("Start query")
    res = [row for row in req_data
           if filter_new_queries_predicate(row)]

    print("Preparing answer")
    answer = {
        "not_exist": res,
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
