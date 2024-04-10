import inspect

from sqlalchemy import Engine

import crud.message_group_id_generator as mgig

from crud.objects.customer import CustomerCRUD
from crud.objects.client import ClientCRUD
from crud.objects.query import QueryCRUD

import datetime


def init_db(engine: Engine) -> None:
    print("start insert_dummy_values")

    ############################################################################
    # Customers.
    customer_1 = {
        "customer_id": "customer_1",
        "black_list": ["fuck", "shit", "nigger"],
    }
    customer_2 = {
        "customer_id": "customer_2",
        "black_list": ["bitch", "freak"],
    }
    print("Start insert customers")
    CustomerCRUD.insert_all([customer_1, customer_2])
    print("Finished insert customers")

    ############################################################################
    # Clients.
    client_1 = {
        "client_id": "client_1",
        "attitude": "arrogant",
    }
    client_2 = {
        "client_id": "client_2",
        "attitude": "famous",
    }
    print("Start insert clients")
    ClientCRUD.insert_all([client_1, client_2])
    print("Finished insert clients")

    ############################################################################
    # Queries.
    query_1 = {
        "customer_id": customer_1["customer_id"],
        "client_id": client_1["client_id"],
        "channel_id": "phystech.career",
        "message": inspect.cleandoc("""Good morning.
            My name is client_1.
            I need Python developers."""),
        "message_group_id": mgig.IdGenerator.reserve_id(),
        "message_date": datetime.datetime.strptime(
                "2023-12-31T22:59:00",
                "%Y-%m-%dT%H:%M:%S"
        ),
    }
    query_2 = {
        "customer_id": customer_2["customer_id"],
        "client_id": client_2["client_id"],
        "channel_id": "phystech.career",
        "message": inspect.cleandoc("""Hi!
            My name is client_2.
            I need C++ developers."""),
        "message_group_id": mgig.IdGenerator.reserve_id(),
        "message_date": datetime.datetime.strptime(
                "2023-12-31T23:59:00",
                "%Y-%m-%dT%H:%M:%S"
        ),
    }
    print("Start insert queries")
    query_id_list = QueryCRUD.insert_all([query_1, query_2])
    print("Finished insert queries")

    ############################################################################
    # Offers.
    offer_1 = {
        "query_id": query_id_list[0],
        "file": "/path/to/offer1",
    }
    offer_2 = {
        "query_id": query_id_list[1],
        "file": "/path/to/offer2",
    }

    print("finished insert_dummy_values")
