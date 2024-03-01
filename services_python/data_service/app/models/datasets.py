from sqlalchemy import Column, String, JSON, text
from sqlalchemy.dialects.postgresql import UUID

from services_python.data_service.app.models.base import Base


class Dataset(Base):
    ID = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()")
    )
    DatasourceID = Column(UUID(as_uuid=True), server_default=text("uuid_generate_v4()"))
    Name = Column(String)
    Other = Column(JSON)
