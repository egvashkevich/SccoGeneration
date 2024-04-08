# Table Configuration with Declarative:
# https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm
# -declarative-table

# Data types.
# https://docs.sqlalchemy.org/en/20/core/type_basics.html#generic-camelcase

# Actual database schema:
# https://miro.com/app/board/uXjVKZsS6Io=/

################################################################################
# Imports.
################################################################################

# Types.
from typing import Optional

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

from type_map import TextType
from type_map import QueryIdType
from type_map import CustomerIdType
from type_map import BlackListType
from type_map import MessageGroupIdType
from type_map import ClientIdType
from type_map import AttitudeType
from type_map import CorporateOfferFileType
from type_map import ServiceIdType
from type_map import ServiceLogStatus
from type_map import ServiceErrorIdType
from type_map import ServiceRejectionIdType
from type_map import LogIdType
from type_map import type_map

################################################################################
# Setup.
################################################################################

# metadata_obj = MetaData(schema="scco_schema")
metadata_obj = MetaData()

# bigint = Annotated[int, "bigint"]


class Base(DeclarativeBase):
    # metadata = metadata_obj
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
################################################################################

# = mapped_column(server_default=func.CURRENT_TIMESTAMP())
# - mapped_column(onupdate=datetime.datetime.now)


# class MyTable(Base):
#     __tablename__ = "my_table"
#     __table_args__ = (
#         PrimaryKeyConstraint("table_id"),
#     )
#
#     table_id: Mapped[int] = mapped_column(autoincrement=True)
#     message: Mapped[TextMapType]


class Query(Base):
    __tablename__ = "query"
    __table_args__ = (
        PrimaryKeyConstraint("query_id"),
        ForeignKeyConstraint(["client_id"], ["client.client_id"]),
        ForeignKeyConstraint(["customer_id"], ["customer.customer_id"]),
        # UniqueConstraint("foo"),
    )

    query_id: Mapped[QueryIdType] = mapped_column(autoincrement=True)
    customer_id: Mapped[CustomerIdType]
    client_id: Mapped[ClientIdType]
    channel_id: Mapped[TextType]
    message: Mapped[TextType]
    message_group_id: Mapped[MessageGroupIdType]
    message_date: Mapped[datetime.date]

    # Relationships.
    customer: Mapped["Customer"] = relationship(
        back_populates="queries"
    )
    client: Mapped["Client"] = relationship(
        back_populates="queries"
    )
    corporate_offer: Mapped["CorporateOffer"] = relationship(
        back_populates="query"
    )


class Customer(Base):
    __tablename__ = "customer"

    customer_id: Mapped[CustomerIdType] = mapped_column(primary_key=True)
    black_list: Mapped[BlackListType]

    # Relationships.
    queries: Mapped["Query"] = relationship(
        back_populates="customer"
    )


class Client(Base):
    __tablename__ = "client"

    client_id: Mapped[ClientIdType] = mapped_column(primary_key=True)
    attitude: Mapped[AttitudeType]

    # Relationships.
    queries: Mapped["Query"] = relationship(
        back_populates="client"
    )


class CorporateOffer(Base):
    __tablename__ = "corporate_offer"
    __table_args__ = (
        PrimaryKeyConstraint("query_id"),
        ForeignKeyConstraint(["query_id"], ["query.query_id"]),
    )

    query_id: Mapped[QueryIdType]
    file: Mapped[CorporateOfferFileType]

    # Relationships.
    query: Mapped["Query"] = relationship(
        back_populates="corporate_offer"
    )

#############################################################################


# class Service(Base):
#     __tablename__ = "service"
#
#     service_id: Mapped[ServiceIdMapType] = mapped_column(primary_key=True)
#     service_name: Mapped[TextMapType]
#
#
# class ServiceLog(Base):
#     __tablename__ = "service_log"
#     __table_args__ = (
#         PrimaryKeyConstraint("log_id"),
#         ForeignKeyConstraint(["query_id"], ["query.query_id"]),
#         ForeignKeyConstraint(["service_id"], ["service.service_id"]),
#         ForeignKeyConstraint(["error_id"], ["service_error.error_id"]),
#         ForeignKeyConstraint(
#             ["rejection_id"],
#             ["service_rejection.rejection_id"]
#         ),
#     )
#
#     log_id: Mapped[LogIdMapType]
#     query_id: Mapped[QueryIdMapType]
#     service_id: Mapped[ServiceIdMapType]
#     log_date: Mapped[datetime.date]
#     service_log_status: Mapped[ServiceLogStatus]
#     error_id: Mapped[Optional[ServiceErrorIdMapType]]
#     rejection_id: Mapped[Optional[ServiceRejectionIdMapType]]
#
#
# class ServiceError(Base):
#     __tablename__ = "service_error"
#
#     error_id: Mapped[ServiceErrorIdMapType] = mapped_column(primary_key=True)
#     error_message: Mapped[TextMapType]
#
#
# class ServiceRejection(Base):
#     __tablename__ = "service_rejection"
#     __table_args__ = (
#         PrimaryKeyConstraint("rejection_id"),
#     )
#
#     rejection_id: Mapped[ServiceRejectionIdMapType]
#     rejection_message: Mapped[TextMapType]


################################################################################

# class ServiceErrorLog(Base):
#     __tablename__ = "service_error_log"
#     __table_args__ = (
#         PrimaryKeyConstraint("log_id"),
#         ForeignKeyConstraint(["query_id"], ["query.query_id"]),
#         ForeignKeyConstraint(["service_id"], ["service.service_id"]),
#         ForeignKeyConstraint(["error_id"], ["service_error.error_id"]),
#     )
#
#     log_id: Mapped[LogIdMapType]
#     query_id: Mapped[QueryIdMapType]
#     service_id: Mapped[ServiceIdMapType]
#     error_id: Mapped[ServiceErrorIdMapType]
#     error_date: Mapped[datetime.date]


# class ServiceRejectionLog(Base):
#     __tablename__ = "service_rejection_log"
#     __table_args__ = (
#         PrimaryKeyConstraint("log_id"),
#         ForeignKeyConstraint(["query_id"], ["query.query_id"]),
#         ForeignKeyConstraint(["service_id"], ["service.service_id"]),
#         ForeignKeyConstraint(["rejection_id"], ["service_rejection.rejection_id"]),
#     )
#
#     log_id: Mapped[LogIdMapType]
#     query_id: Mapped[QueryIdMapType]
#     service_id: Mapped[ServiceIdMapType]
#     rejection_id: Mapped[ServiceRejectionIdMapType]
#     rejection_date: Mapped[datetime.date]


################################################################################

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
