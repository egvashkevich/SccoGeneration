import util.parse_env as pe

################################################################################
# Global setup.

RMQ_NET_ALIAS = pe.get_or_default(
    "RMQ_NET_ALIAS",
    "not_presented"
)

DB_FUNCTIONAL_SERVICE_EXCHANGE = pe.get_or_default(
    "DB_FUNCTIONAL_SERVICE_EXCHANGE",
    "not_presented",
)
DB_FUNCTIONAL_SERVICE_QUEUE = pe.get_or_default(
    "DB_FUNCTIONAL_SERVICE_QUEUE",
    "not_presented"
)
DB_FUNCTIONAL_SERVICE_ROUTING_KEY = pe.get_or_default(
    "DB_FUNCTIONAL_SERVICE_ROUTING_KEY",
    "not_presented"
)

POSTGRES_FS_ALIAS = pe.get_or_default(
    "POSTGRES_FS_ALIAS",
    "not_presented"
)

################################################################################
# Local setup.

POSTGRES_USER = pe.get_or_default(
    "POSTGRES_USER",
    "not_presented"
)
POSTGRES_PASSWORD = pe.get_or_default(
    "POSTGRES_PASSWORD",
    "not_presented"
)
POSTGRES_PORT = pe.get_or_default(
    "POSTGRES_PORT",
    "not_presented"
)
POSTGRES_DB = pe.get_or_default(
    "POSTGRES_DB",
    "not_presented"
)

_IS_ON_HOST_BOOL = pe.contains("IS_ON_HOST")


def is_on_host() -> bool:
    return _IS_ON_HOST_BOOL


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
