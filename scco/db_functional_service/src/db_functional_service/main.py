import sys

import crud.dbapi as dbapi
from crud.models import Base

from db_functional_service.broker.rmq_broker import RmqBroker
from db_functional_service.dispatcher import Dispatcher
from db_functional_service.data.init_db import dummy_init_db


def fake_init_db_data():
    dummy_init_db()


def init_database():
    print("Creating db engine", flush=True)
    engine = dbapi.DbEngine.get_engine()

    print("Removing old tables", flush=True)
    Base.metadata.drop_all(engine)

    print("Creating tables", flush=True)
    Base.metadata.create_all(engine)

    print("Inserting dummy values", flush=True)
    fake_init_db_data()


def main():
    init_database()

    print("Creating broker", flush=True)
    broker = RmqBroker()

    print("Creating dispatcher", flush=True)
    dispatcher = Dispatcher(broker)

    print("Start consuming", flush=True)
    broker.start_consuming()  # Infinite loop.


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted', file=sys.stderr)
    except Exception as e:
        print(f'Internal service unexpected error: {e}', file=sys.stderr)
        sys.exit(2)
