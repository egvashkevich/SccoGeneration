from sqlalchemy import insert

from sqlalchemy.orm import Session

from crud.models import Customer

import crud.dbapi as dbapi


class CustomerCRUD:
    def __init__(self):
        pass

    @classmethod
    def insert_one(cls, customer: dict) -> None:
        cls.insert_all([customer])

    @classmethod
    def insert_all(cls, customers: list[dict]) -> None:
        if len(customers) == 0:
            return

        # TODO: add validation
        engine = dbapi.DbEngine.get_engine()
        with Session(engine) as session:
            stmt = insert(Customer).values(customers)
            with session.begin():
                session.execute(stmt)
