from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import func as sqlfunc

from crud.models import Query
from crud.util import json_get_or_panic
import crud.dbapi as dbapi

import json


def contains_query_predicate(row, session):
    """
    :return: true, if database contains row.
    """
    print("Enter contains_query_predicate")
    stmt = (select(sqlfunc.count())
            .select_from(Query)
            .where(Query.customer_id == row["customer_id"])
            .where(Query.client_id == row["client_id"])
            .where(Query.channel_id == row["channel_id"])
            .where(Query.message_date == row["message_date"])
            .limit(1))
    print("Make contains_query_predicate")
    res = (session.scalars(stmt).one() == 0)
    print("Done contains_query_predicate")
    return res  # without raws


def contains_query(query_data, reply, db_query):
    # Check keys.
    required_keys = [
        "customer_id",
        "client_id",
        "channel_id",
        "message_date",
    ]

    for row in query_data:
        for key in required_keys:
            json_get_or_panic(row, key, db_query)

    # Make db query.
    print("Start query")
    engine = dbapi.DbEngine.get_engine()
    with Session(engine) as session:
        answer = [row for row in query_data
                  if contains_query_predicate(row, session)]
    print("Finish query")

    # Send query to rabbitmq.
    answer = json.dumps(answer, indent=2)
    print(f"Answer:\n'{answer}'")
    # ...
