import enum

from typing import Any
from typing import Dict
from typing import Type

from sqlalchemy import types
from sqlalchemy.types import TypeEngine

import datetime
import decimal
import uuid


class TextMapType:
    pass


class ClientIdMapType:
    pass


class AttitudeMapType:
    pass


class QueryIdMapType:
    pass


class CorporateOfferFileMapType:
    pass


class ServiceIdMapType:
    pass


class ServiceLogProcessStatus(enum.Enum):
    START = "start"
    FINISH = "finish"


class ServiceErrorIdMapType:
    pass


class ServiceRejectionIdMapType:
    pass


QueryIdType = int
ServiceIdType = int
ServiceErrorIdType = int
RejectionIdType = int

################################################################################

# default type mapping, deriving the type for mapped_column()
# from a Mapped[] annotation
type_map: Dict[Type[Any], TypeEngine[Any]] = {
    # Default
    bool: types.Boolean(),
    bytes: types.LargeBinary(),
    datetime.date: types.Date(),
    datetime.datetime: types.DateTime(),
    datetime.time: types.Time(),
    datetime.timedelta: types.Interval(),
    decimal.Decimal: types.Numeric(),
    float: types.Float(),
    int: types.Integer(),
    str: types.String(),
    uuid.UUID: types.Uuid(),

    # Custom
    TextMapType: types.Text,
    QueryIdMapType: QueryIdType,
    ClientIdMapType: types.Text,
    AttitudeMapType: types.Text,
    CorporateOfferFileMapType: types.Text,
    ServiceIdMapType: ServiceIdType,
    ServiceErrorIdMapType: ServiceErrorIdType,
    ServiceRejectionIdMapType: RejectionIdType,
    # str: String().with_variant(String(255), "mysql", "mariadb"),
    # bigint: BigInteger()
}
