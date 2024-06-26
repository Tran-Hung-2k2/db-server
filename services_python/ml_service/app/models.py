from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column,
    Integer,
    String,
    JSON,
    DateTime,
    ForeignKey,
    text,
)


class Base(declarative_base(), SerializerMixin):
    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        unique=True,
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )
    description = Column(
        String,
        nullable=True,
    )
    other = Column(JSON)


class Project(Base):
    __tablename__ = "projects"

    user_id = Column(
        UUID(as_uuid=True),
        nullable=False,
    )
    name = Column(
        String,
        nullable=False,
    )
    flow = Column(
        String,
        nullable=True,
        unique=False,
    )
    experiment_id = Column(
        Integer,
        nullable=True,
    )
    deployment_id = Column(
        UUID(as_uuid=True),
        nullable=True,
    )
    config = Column(JSON)


class Run(Base):
    __tablename__ = "runs"

    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    name = Column(
        String,
        nullable=False,
    )
    flow_run_id = Column(
        String,
        nullable=True,
        unique=True,
    )
    run_id = Column(
        String,
        nullable=True,
        unique=True,
    )


class Model(Base):
    __tablename__ = "models"

    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    run_id = Column(
        UUID(as_uuid=True),
        ForeignKey("runs.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    name = Column(
        String,
        nullable=True,
    )
    version = Column(
        Integer,
        nullable=False,
    )
