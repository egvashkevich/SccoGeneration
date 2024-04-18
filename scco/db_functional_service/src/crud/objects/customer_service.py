from sqlalchemy import insert

from sqlalchemy.orm import Session

from crud.models import CustomerService

import crud.dbapi as dbapi

from crud.base.SelectorBase import SelectorBase


class CustomerServiceCRUD(SelectorBase):
    def __init__(self):
        pass

    @classmethod
    def insert_one(cls, customer_service: dict) -> None:
        cls.insert_all([customer_service])

    @classmethod
    def insert_all(cls, customer_services: list[dict]) -> None:
        if len(customer_services) == 0:
            print("CustomerServiceCRUD::insert_all: no customer_services")
            return

        # TODO: add validation
        engine = dbapi.DbEngine.get_engine()
        with Session(engine) as session:
            stmt = insert(CustomerService).values(customer_services)
            with session.begin():
                session.execute(stmt)

    # # TODO
    # @classmethod
    # def update_all(cls, customer_services: list[dict]):
    #     pass
