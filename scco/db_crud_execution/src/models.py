# Table Configuration with Declarative:
# https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm
# -declarative-table

# Data types.
# https://docs.sqlalchemy.org/en/20/core/type_basics.html#generic-camelcase

################################################################################
# Imports.
################################################################################

# Types.
from typing import Any
from typing import Dict
from typing import Type

from sqlalchemy import types
from sqlalchemy.types import TypeEngine

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# Tables.
from sqlalchemy import ForeignKey

from sqlalchemy import MetaData

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import UniqueConstraint

import datetime
import decimal
import uuid

from type_map import TextMapType
from type_map import QueryIdMapType
from type_map import ClientIdMapType
from type_map import AttitudeMapType
from type_map import CorporateOfferFileMapType
from type_map import ServiceIdMapType
from type_map import ServiceLogProcessStatus
from type_map import ServiceErrorIdMapType
from type_map import ServiceRejectionIdMapType
from type_map import type_map

################################################################################
# Setup.
################################################################################

metadata_obj = MetaData(schema="some_schema")

# bigint = Annotated[int, "bigint"]


class Base(DeclarativeBase):
    metadata = metadata_obj
    registry = registry(
        type_annotation_map=type_map,
        # type_annotation_map={
        #     # str_30: String(30),
        #     # str_50: String(50),
        #     # num_12_4: Numeric(12, 4),
        #     # num_6_2: Numeric(6, 2),
        # }
    )

################################################################################

# Models.


class Query(Base):
    __tablename__ = "query"
    __table_args__ = (
        PrimaryKeyConstraint("query_id"),
        ForeignKeyConstraint(["client_id"], ["client.client_id"]),
        # UniqueConstraint("foo"),
    )

    query_id: Mapped[QueryIdMapType]
    client_id: Mapped[ClientIdMapType]
    message: Mapped[TextMapType]
    channel_id: Mapped[TextMapType]
    message_date: Mapped[datetime.date]


class Client(Base):
    __tablename__ = "client"

    client_id: Mapped[ClientIdMapType] = mapped_column(primary_key=True)
    attitude: Mapped[AttitudeMapType]


class CorporateOffer(Base):
    __tablename__ = "corporate_offer"
    __table_args__ = (
        PrimaryKeyConstraint("query_id"),
        ForeignKeyConstraint(["query_id"], ["query.query_id"]),
    )

    query_id: Mapped[QueryIdMapType]
    file: Mapped[CorporateOfferFileMapType]


class Service(Base):
    __tablename__ = "service"

    service_id: Mapped[ServiceIdMapType] = mapped_column(primary_key=True)
    service_name: Mapped[TextMapType]


class ServiceLog(Base):
    __tablename__ = "service_log"
    __table_args__ = (
        PrimaryKeyConstraint("query_id", "service_id", "process_status"),
        ForeignKeyConstraint(["query_id"], ["query.query_id"]),
        ForeignKeyConstraint(["service_id"], ["service.service_id"]),
    )

    query_id: Mapped[QueryIdMapType]
    service_id: Mapped[ServiceIdMapType]
    log_date: Mapped[datetime.date]
    process_status: Mapped[ServiceLogProcessStatus]


class ServiceErrorLog(Base):
    __tablename__ = "service_error_log"
    __table_args__ = (
        PrimaryKeyConstraint("query_id", "service_id", "error_code"),
        ForeignKeyConstraint(["query_id"], ["query.query_id"]),
        ForeignKeyConstraint(["service_id"], ["service.service_id"]),
        ForeignKeyConstraint(["error_id"], ["service_error.error_id"]),
    )

    query_id: Mapped[QueryIdMapType]
    service_id: Mapped[ServiceIdMapType]
    error_id: Mapped[ServiceErrorIdMapType]
    error_date: Mapped[datetime.date]


class ServiceError(Base):
    __tablename__ = "service_error"

    error_id: Mapped[ServiceErrorIdMapType] = mapped_column(primary_key=True)
    error_description: Mapped[TextMapType]


class ServiceRejectionLog(Base):
    __tablename__ = "service_rejection_log"
    __table_args__ = (
        PrimaryKeyConstraint("query_id", "service_id", "rejection_log"),
        ForeignKeyConstraint(["query_id"], ["query.query_id"]),
        ForeignKeyConstraint(["service_id"], ["service.service_id"]),
        ForeignKeyConstraint(["rejection_id"], ["service_rejection.rejection_id"]),
    )

    query_id: Mapped[QueryIdMapType]
    service_id: Mapped[ServiceIdMapType]
    rejection_id: Mapped[ServiceRejectionIdMapType]
    rejection_date: Mapped[datetime.date]


class ServiceRejection(Base):
    __tablename__ = "service_rejection"
    __table_args__ = (
        PrimaryKeyConstraint("rejection_id"),
    )

    rejection_id: Mapped[ServiceRejectionIdMapType]
    error_description: Mapped[TextMapType]


################################################################################

