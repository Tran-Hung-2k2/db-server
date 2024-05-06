from pydantic import BaseModel, UUID4
from typing import Optional


class DatasetCreate(BaseModel):
    name: str
    user_id: Optional[UUID4] = None
    other: Optional[dict] = None

class DatasetUpdate(BaseModel):
    name: str
    other: Optional[dict] = None

