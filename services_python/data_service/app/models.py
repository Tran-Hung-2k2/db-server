from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
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

    # def to_dict(self):
    #     return {
    #         col.name: (
    #             str(getattr(self, col.name))
    #             if isinstance(col.type, (UUID, db.DateTime))
    #             else getattr(self, col.name)
    #         )
    #         for col in self.__table__.columns
    #     }


class DatasourceType(Base):
    __tablename__ = "datasource_types"

    name = db.Column(db.String, nullable=False, unique=True)

    # Định nghĩa mối quan hệ một nhiều với bảng Datasource
    datasources = relationship("Datasource", back_populates="datasource_type")

    # Serialization rules
    serialize_rules = ("-datasources",)


class Datasource(Base):
    __tablename__ = "datasources"

    user_id = db.Column(UUID(as_uuid=True), nullable=False)
    type_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("datasource_types.id"), nullable=False
    )
    name = db.Column(db.String, nullable=False)
    host = db.Column(db.String, nullable=False)
    port = db.Column(db.String, nullable=False)
    other = db.Column(db.JSON)

    # Định nghĩa mối quan hệ nhiều một với bảng DatasourceType
    datasource_type = relationship("DatasourceType", back_populates="datasources")
    # Định nghĩa mối quan hệ một nhiều với bảng Dataset
    datasets = relationship("Dataset", back_populates="datasource")

    # Serialization rules
    serialize_rules = ("-datasets",)


class Dataset(Base):
    __tablename__ = "datasets"

    datasource_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("datasources.id"),
    )
    name = db.Column(db.String, nullable=False)
    other = db.Column(db.JSON)

    # Định nghĩa mối quan hệ nhiều một với bảng Datasource
    datasource = relationship("Datasource", back_populates="datasets")
    # Định nghĩa mối quan hệ một nhiều với bảng DatasetVersion
    dataset_versions = relationship("DatasetVersion", back_populates="dataset")

    # Serialization rules
    serialize_rules = ("-dataset_versions",)


class DatasetVersion(Base):
    __tablename__ = "dataset_versions"

    dataset_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("datasets.id"),
        nullable=False,
    )
    name = db.Column(db.String, nullable=False)
    schema = db.Column(db.JSON)
    other = db.Column(db.JSON)

    # Định nghĩa mối quan hệ nhiều một với bảng Dataset
    dataset = relationship("Dataset", back_populates="dataset_versions")
