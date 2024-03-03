import sys

sys.path.append(".")

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import sqlalchemy as db


class Base(declarative_base()):
    __abstract__ = True
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now()
    )

    def to_dict(self):
        return {
            col.name: (
                str(getattr(self, col.name))
                if isinstance(col.type, (UUID, db.DateTime))
                else getattr(self, col.name)
            )
            for col in self.__table__.columns
        }


class Datasource(Base):
    __tablename__ = "datasources"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=db.text("uuid_generate_v4()"),
    )
    user_id = db.Column(
        UUID(as_uuid=True), nullable=False, server_default=db.text("uuid_generate_v4()")
    )
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    host = db.Column(db.String, nullable=False)
    port = db.Column(db.String, nullable=False)
    other = db.Column(db.JSON)
    # Định nghĩa mối quan hệ một nhiều với bảng Dataset
    datasets = relationship("Dataset", back_populates="datasource")


class Dataset(Base):
    __tablename__ = "datasets"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=db.text("uuid_generate_v4()"),
    )
    datasource_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("datasources.id"),
        nullable=False,
        server_default=db.text("uuid_generate_v4()"),
    )
    name = db.Column(db.String, nullable=False)
    other = db.Column(db.JSON)
    # Định nghĩa mối quan hệ nhiều một với bảng Datasource
    datasource = relationship("Datasource", back_populates="datasets")
    # Định nghĩa mối quan hệ một nhiều với bảng DatasetVersion
    dataset_versions = relationship("DatasetVersion", back_populates="dataset")


class DatasetVersion(Base):
    __tablename__ = "dataset_versions"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=db.text("uuid_generate_v4()"),
    )
    dataset_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("datasets.id"),
        nullable=False,
        server_default=db.text("uuid_generate_v4()"),
    )
    name = db.Column(db.String, nullable=False)
    schema = db.Column(db.JSON)
    other = db.Column(db.JSON)
    # Định nghĩa mối quan hệ nhiều một với bảng Dataset
    dataset = relationship("Dataset", back_populates="dataset_versions")
