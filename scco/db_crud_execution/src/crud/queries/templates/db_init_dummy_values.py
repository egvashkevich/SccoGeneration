from sqlalchemy import Engine
from sqlalchemy.orm import Session

import crud.message_group_id_generator as mgig

from crud.models import Customer
from crud.models import Client
from crud.models import Query
from crud.models import CorporateOffer

import datetime


def db_init_dummy_values(engine: Engine) -> None:
    print("start insert_dummy_values")
    with Session(engine) as session:
        print("session start")

        # Customers.
        customer_1 = Customer(
            customer_id="customer_1",
            black_list=["fuck", "shit", "nigger"]
        )
        customer_2 = Customer(
            customer_id="customer_2",
            black_list=["bitch", "freak"]
        )
        print("Start insert customers")
        session.add_all([customer_1, customer_2])
        session.commit()
        print("Finished insert customers")

        # Clients.
        client_1 = Client(
            client_id="client_1",
            attitude="arrogant",
        )
        client_2 = Client(
            client_id="client_2",
            attitude="famous",
        )
        print("Start insert clients")
        session.add_all([client_1, client_2])
        session.commit()
        print("Finished insert clients")

        # Queries.
        query_1 = Query(
            customer_id=customer_1.customer_id,
            client_id=client_1.client_id,
            channel_id="phystech.career",
            message="""Good morning.
            My name is client_1.
            I need Python developers.""",
            message_group_id=mgig.IdGenerator.reserve_id(),
            message_date=datetime.datetime.strptime(
                "2023-12-31T22:59:00",
                "%Y-%m-%dT%H:%M:%S"
            ),
        )
        query_2 = Query(
            customer_id=customer_1.customer_id,
            client_id=client_2.client_id,
            channel_id="phystech.career",
            message="""Hi!
            My name is client_2.
            I need C++ developers.""",
            message_group_id=mgig.IdGenerator.reserve_id(),
            message_date=datetime.datetime.strptime(
                "2023-12-31T23:59:00",
                "%Y-%m-%dT%H:%M:%S"
            ),
        )
        print("Start insert queries")
        session.add_all([query_1, query_2])
        session.commit()
        print("Finished insert queries")

        # session.commit()

    print("finished insert_dummy_values")
