from pydantic import BaseModel, UUID4
from typing import Optional


class DatasetCreate(BaseModel):
    name: str
    user_id: Optional[UUID4] = None
    description: Optional[str] = None


class DatasetUpdate(BaseModel):
    name: str
    description: Optional[str] = None
