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
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now()
    )


class Jobset(Base):
    __tablename__ = "jobsets"

    user_id = db.Column(UUID(as_uuid=True), nullable=False)
    name = db.Column(db.String, nullable=False)
    other = db.Column(db.JSON)
