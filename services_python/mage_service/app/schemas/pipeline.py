from pydantic import BaseModel, UUID4
from typing import Optional


class PipelineCreate(BaseModel):
    name: str
    type: str
    description: Optional[str] = None


class PipelineUpdate(BaseModel):
    name: str
    other: Optional[dict] = None

class BlockCreate(BaseModel):
    name: str
    block_type:str
    source_type:str
    source_config:str
    description: Optional[str] = None

class BlockUpdate(BaseModel):
    name: str
    block_type: Optional[str] = None
    source_type: Optional[str] = None
    source_config: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    downstream_blocks: Optional[list] = None
    upstream_blocks: Optional[list] = None
    conditional_blocks: Optional[list] = None
    callback_blocks: Optional[list] = None
    has_callback: Optional[bool] = None
    retry_config: Optional[dict] = None

class PipelineScheduleCreate(BaseModel):
    name: str
    schedule_type: str
    schedule_interval: str
    start_time: str
    description: Optional[str] = None
    settings: Optional[dict] = None

class PipelineScheduleUpdate(BaseModel):
    name: str
    status : str
    schedule_type: Optional[str] = None
    schedule_interval: Optional[str] = None
    start_time: Optional[str] = None
    description: Optional[str] = None
    settings: Optional[dict] = None
    tags: Optional[list] = None