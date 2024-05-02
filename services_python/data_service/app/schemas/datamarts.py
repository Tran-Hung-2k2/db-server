from pydantic import BaseModel, UUID4
from typing import Optional


class DatamartCreate(BaseModel):
    name: str
    user_id: Optional[UUID4] = None
    other: Optional[dict] = None


class DatamartUpdate(BaseModel):
    name: str
    other: Optional[dict] = None
