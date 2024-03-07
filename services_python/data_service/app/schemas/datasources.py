from pydantic import BaseModel, UUID4, constr
from typing import Optional


class DatasourceCreate(BaseModel):
    name: str
    type_id: UUID4
    host: str
    port: constr(strip_whitespace=True, pattern=r"^[1-9]\d*$")
    user_id: Optional[UUID4] = None
    other: Optional[dict] = None


class DatasourceUpdate(BaseModel):
    name: str
    type_id: UUID4
    host: str
    port: constr(strip_whitespace=True, pattern=r"^[1-9]\d*$")
    other: Optional[dict] = None
