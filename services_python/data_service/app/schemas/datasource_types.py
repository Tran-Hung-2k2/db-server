from pydantic import BaseModel


class DatasourceTypeCreate(BaseModel):
    name: str


class DatasourceTypeUpdate(BaseModel):
    name: str
