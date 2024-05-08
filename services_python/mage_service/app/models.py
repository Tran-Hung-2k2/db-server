from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as db


class Base(declarative_base(), SerializerMixin):
    __abstract__ = True

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=db.text("uuid_generate_v4()"),
    )
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now()
    )


class Pipeline(Base):
    __tablename__ = "pipelines"
    user_id = db.Column(UUID(as_uuid=True), nullable=False)
    pipeline_type = db.Column(db.String, nullable=False)
    

class Block(Base):
    __tablename__ = "blocks"
    pipeline_id = db.Column(UUID(as_uuid=True), db.ForeignKey('pipelines.id'), nullable=False)
    source_type = db.Column(db.String, nullable=False)
    source_config = db.Column(db.String, nullable=False)
    block_type = db.Column(db.String, nullable=False)

class PipelineSchedule(Base):
    __tablename__ = "pipeline_schedules"
    user_id = db.Column(UUID(as_uuid=True), nullable=False)
    pipeline_id = db.Column(UUID(as_uuid=True), nullable=False)
    pipeline_schedule_type = db.Column(db.String, nullable=False)
