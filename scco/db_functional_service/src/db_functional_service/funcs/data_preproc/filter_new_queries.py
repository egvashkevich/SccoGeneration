from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import func as sqlfunc

from util.json_handle import dict_has_or_panic
import crud.dbapi as dbapi

# TODO: replace with QueryCRUD
from crud.models import Query

import json

import util.parse_env as ps

import db_functional_service.rmq_handle as rmq

from util.reply_ctx import add_reply_ctx


def filter_new_queries_predicate(row, session):
    """
    :return: true, if database contains row.
    """
    print("Enter filter_new_queries_predicate")
    stmt = (select(sqlfunc.count())
            .select_from(Query)
            .where(Query.customer_id == row["customer_id"])
            .where(Query.client_id == row["client_id"])
            .where(Query.channel_id == row["channel_id"])
            .where(Query.message_date == row["message_date"])
            .limit(1))
    print("Make filter_new_queries_predicate")
    res = (session.scalars(stmt).one() == 0)
    print("Done filter_new_queries_predicate")
    return res  # without raws


def filter_new_queries(req_data, reply, srv_req_data):
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
    engine = dbapi.DbEngine.get_engine()
    with Session(engine) as session:
        res = [row for row in req_data
               if filter_new_queries_predicate(row, session)]
    print("Finish query")
    answer = {
        "not_exist": res,
    }

    # Add reply_ctx.
    add_reply_ctx(srv_req_data, answer)

    # Send query to rabbitmq.
    answer = json.dumps(answer, indent=2)
    print(f"Answer:\n{answer}")

    if not ps.is_on_host():
        rmq.RmqHandle.basic_publish(answer, reply)
