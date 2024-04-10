from sqlalchemy import insert
from sqlalchemy.orm import Session

from crud.models import Offer

import crud.dbapi as dbapi


class OfferCRUD:
    def __init__(self):
        pass

    @classmethod
    def insert_one(cls, offer_dict: dict) -> None:
        cls.insert_all([offer_dict])

    @classmethod
    def insert_all(cls, offer_dicts: list[dict]) -> None:
        # TODO: add validation
        engine = dbapi.DbEngine.get_engine()
        with Session(engine) as session:
            stmt = insert(Offer)
            with session.begin():
                session.execute(stmt, offer_dicts)
