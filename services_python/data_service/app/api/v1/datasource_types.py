from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request
from pydantic import UUID4

from services_python.data_service.app.database import get_session
import services_python.data_service.app.controllers.datasource_types as ctl
import services_python.data_service.app.schemas.datasource_types as schemas
import services_python.middlewares.auth as middlewares

router = APIRouter(prefix="/datasource_types", tags=["DatasourceTypes"])


@router.get("/", dependencies=[Depends(middlewares.verify_all)])
async def get_datasource_types(
    request: Request,
    db: Session = Depends(get_session),
):
    return ctl.get_datasource_types(db, request)


@router.post("/", dependencies=[Depends(middlewares.verify_admin)])
async def create_datasource_type(
    data: schemas.DatasourceTypeCreate, db: Session = Depends(get_session)
):
    return ctl.create_datasource_type(db, data)


@router.put("/{id}", dependencies=[Depends(middlewares.verify_admin)])
async def update_datasource_type(
    id: UUID4,
    data: schemas.DatasourceTypeUpdate,
    db: Session = Depends(get_session),
):
    return ctl.update_datasource_type(db, id, data)


@router.delete("/{id}", dependencies=[Depends(middlewares.verify_admin)])
async def delete_datasource_type(id: UUID4, db: Session = Depends(get_session)):
    return ctl.delete_datasource_type(db, id)
