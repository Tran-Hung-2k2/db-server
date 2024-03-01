import sys

sys.path.append(".")

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, JSON, DateTime, func, text
from sqlalchemy.dialects.postgresql import UUID


class Base(declarative_base()):
    __abstract__ = True
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Datasource(Base):
    __tablename__ = "datasources"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()")
    )
    user_id = Column(UUID(as_uuid=True), server_default=text("uuid_generate_v4()"))
    name = Column(String)
    type = Column(String)
    host = Column(String)
    port = Column(String)
    other = Column(JSON)


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()")
    )
    datasource_id = Column(
        UUID(as_uuid=True), server_default=text("uuid_generate_v4()")
    )
    name = Column(String)
    other = Column(JSON)


class DatasetVersion(Base):
    __tablename__ = "dataset_versions"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()")
    )
    dataset_id = Column(UUID(as_uuid=True), server_default=text("uuid_generate_v4()"))
    name = Column(String)
    schema = Column(JSON)
    other = Column(JSON)
