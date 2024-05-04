from pydantic import BaseModel, UUID4
from typing import Optional


class PipelineCreate(BaseModel):
    name: str
    user_id: Optional[UUID4] = None
    other: Optional[dict] = None

class PipelineUpdate(BaseModel):
    name: str
    other: Optional[dict] = None

