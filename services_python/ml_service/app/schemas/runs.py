from pydantic import BaseModel, UUID4
from typing import Optional


class RunCreate(BaseModel):
    name: Optional[str] = None
    project_id: Optional[UUID4] = None
    flow_run_id: Optional[UUID4] = None
    run_id: Optional[str] = None
    config: dict
    other: Optional[dict] = None
