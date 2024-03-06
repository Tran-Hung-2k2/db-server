from pydantic import BaseModel, UUID4, constr
from fastapi import FileUpload
from typing import Optional, Literal


class DatasourceCreate(BaseModel):
    name: str
    type: Literal["kafka", "postgres"]
    host: str
    port: constr(strip_whitespace=True, pattern=r"^[1-9]\d*$")
    user_id: Optional[UUID4] = None
    other: Optional[dict] = None


class DatasourceUpdate(BaseModel):
    name: str
    type: Literal["kafka", "postgres"]
    host: str
    port: constr(strip_whitespace=True, pattern=r"^[1-9]\d*$")
    other: Optional[dict] = None


class DatasetCreate(BaseModel):
    name: str
    datasource_id: Optional[UUID4] = None
    upload_file: Optional[FileUpload] = None
    other: Optional[dict] = None


class DatasetUpdate(BaseModel):
    name: str
    datasource_id: UUID4
    other: Optional[dict] = None


class DatasetVersionCreate(BaseModel):
    name: str
    dataset_id: UUID4
    other: Optional[dict] = None


class DatasetVersionUpdate(BaseModel):
    name: str
    datasource_id: UUID4
    other: Optional[dict] = None
