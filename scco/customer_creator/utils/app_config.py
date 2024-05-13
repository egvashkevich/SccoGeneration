import util.parse_env as pe

################################################################################
# Global setup.

RMQ_NET_ALIAS = pe.get_or_default(
    "RMQ_NET_ALIAS",
    "not_presented"
)
# ----------------------------------------------------------

CUSTOMER_CREATOR_EXCHANGE = pe.get_or_default(
    "CUSTOMER_CREATOR_EXCHANGE",
    "not_presented"
)
CUSTOMER_CREATOR_QUEUE = pe.get_or_default(
    "CUSTOMER_CREATOR_QUEUE",
    "not_presented"
)
CUSTOMER_CREATOR_ROUTING_KEY = pe.get_or_default(
    "CUSTOMER_CREATOR_ROUTING_KEY",
    "not_presented"
)
# ----------------------------------------------------------

################################################################################
# Local setup.


