from pydantic import BaseModel, UUID4
from typing import Optional


class DatasetCreate(BaseModel):
    name: str
    datasource_id: Optional[UUID4] = None
    other: Optional[dict] = None

class DatasetUpdate(BaseModel):
    name: str
    other: Optional[dict] = None


class DatasetVersionCreate(BaseModel):
    name: str
    dataset_id: UUID4
    other: Optional[dict] = None


class DatasetVersionUpdate(BaseModel):
    name: str
    datasource_id: UUID4
    other: Optional[dict] = None
