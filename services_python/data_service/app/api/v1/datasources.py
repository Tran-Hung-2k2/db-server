from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request
from pydantic import UUID4

from services_python.data_service.app.database import get_session
import services_python.data_service.app.controllers.datasources as ctl
import services_python.data_service.app.schemas as schemas
import services_python.middlewares.auth as middlewares

router = APIRouter(prefix="/datasources", tags=["Datasources"])


@router.get("/", dependencies=[Depends(middlewares.verify_admin)])
async def get_datasources(
    request: Request,
    db: Session = Depends(get_session),
):
    return ctl.get_datasources(db, **dict(request.query_params))


@router.post("/")
async def create_datasource(
    data: schemas.DatasourceCreate, db: Session = Depends(get_session)
):
    return ctl.create_datasource(db, data)


@router.put("/{id}")
async def update_datasource(
    id: UUID4, data: schemas.DatasourceUpdate, db: Session = Depends(get_session)
):
    return ctl.update_datasource(db, id, data)


@router.delete("/{id}")
async def delete_datasource(id: UUID4, db: Session = Depends(get_session)):
    return ctl.delete_datasource(db, id)
