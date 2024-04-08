import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from parse_env import EnvVars


# Engine URL: "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
class DbEngine:
    _engine: Engine = None

    @classmethod
    def get_engine(cls) -> Engine:
        if cls._engine is None:
            cls._engine = cls._create_db_engine()
        return cls._engine

    @staticmethod
    def _create_db_engine() -> Engine:
        postgres_user = EnvVars["POSTGRES_USER"]
        postgres_password = EnvVars["POSTGRES_PASSWORD"]
        if EnvVars.is_on_host():
            EnvVars.set_val("POSTGRES_HOST", "localhost")
            postgres_host = "localhost"
        else:
            postgres_host = EnvVars["POSTGRES_HOST"]
        postgres_port = EnvVars["POSTGRES_PORT"]
        postgres_db = EnvVars["POSTGRES_DB"]

        url = (f"postgresql+psycopg2://{postgres_user}:{postgres_password}@"
               f"{postgres_host}:{postgres_port}/{postgres_db}")

        return create_engine(
            url,
            # pool_recycle=3600,
            echo=True,
            echo_pool=True,
        )
