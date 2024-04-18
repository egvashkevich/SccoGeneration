from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

import util.parse_env as pe


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
        postgres_user = pe._EnvVars["POSTGRES_USER"]
        postgres_password = pe._EnvVars["POSTGRES_PASSWORD"]
        if pe._EnvVars.is_on_host():
            postgres_host = "localhost"
        else:
            postgres_host = pe._EnvVars["POSTGRES_FS_ALIAS"]
        print(f"postgres_host = {postgres_host}")

        postgres_port = pe._EnvVars["POSTGRES_PORT"]
        postgres_db = pe._EnvVars["POSTGRES_DB"]

        url = (f"postgresql+psycopg2://{postgres_user}:{postgres_password}@"
               f"{postgres_host}:{postgres_port}/{postgres_db}")

        return create_engine(
            url,
            # pool_recycle=3600,
            echo=True,
            echo_pool=True,
        )
