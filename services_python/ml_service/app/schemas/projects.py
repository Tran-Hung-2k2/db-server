from pydantic import BaseModel, UUID4
from typing import Optional


class ProjectCreate(BaseModel):
    name: str
    user_id: Optional[UUID4] = None
    experiment_id: Optional[int] = None
    other: Optional[dict] = None


class ProjectUpdate(BaseModel):
    name: str
    other: Optional[dict] = None


class ProjectConfig(BaseModel):
    flow: str
    deployment_id: Optional[UUID4] = None
    config: dict
    other: Optional[dict] = None
