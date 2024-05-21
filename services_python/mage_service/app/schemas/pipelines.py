from pydantic import BaseModel, UUID4
from typing import Optional, Literal


class PipelineCreate(BaseModel):
    name: str
    type: Literal["stream", "batch"]
    description: Optional[str] = None


class PipelineUpdate(BaseModel):
    name: str
    description: Optional[str] = None


class BlockCreate(BaseModel):
    name: str
    block_type: Literal["data_loader", "transformer", "data_exporter"]
    source_type: str
    source_config: str
    description: Optional[str] = None


class BlockUpdate(BaseModel):
    name: Optional[str] = None
    block_type: Optional[Literal["data_loader", "transformer", "data_exporter"]] = "data_loader"
    source_type: Optional[str] = None
    source_config: Optional[str] = None
    description: Optional[str] = None
    downstream_blocks: Optional[list] = []
    upstream_blocks: Optional[list] = []
    conditional_blocks: Optional[list] = []
    callback_blocks: Optional[list] = []
    has_callback: Optional[bool] = False
    retry_config: Optional[dict] = []


class PipelineScheduleCreate(BaseModel):
    name: str
    id: str
    schedule_type: Literal["api", "time"]
    schedule_interval: Literal["@once", "@hourly"]
    start_time: str
    description: Optional[str] = None
    settings: Optional[dict] = None


class PipelineScheduleUpdate(BaseModel):
    name: str
    status: Literal["active", "inactive"]
    schedule_type: Optional[str] = None
    schedule_interval: Optional[str] = None
    start_time: Optional[str] = None
    description: Optional[str] = None
    settings: Optional[dict] = None
    tags: Optional[list] = None
