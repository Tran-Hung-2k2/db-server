from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request
from pydantic import UUID4

from services_python.data_service.app.database import get_session
import services_python.data_service.app.controllers.datasources as ctl
import services_python.data_service.app.schemas as schemas
import services_python.middlewares.auth as middlewares

router = APIRouter(prefix="/datasets", tags=["Datasets"])


@router.get("/", dependencies=[Depends(middlewares.verify_all)])
async def get_datasets(
    request: Request,
    db: Session = Depends(get_session),
):
    return ctl.get_datasets(db, request)


@router.post("/", dependencies=[Depends(middlewares.verify_user)])
async def create_dataset(
    request: Request, data: schemas.DatasourceCreate, db: Session = Depends(get_session)
):
    return ctl.create_dataset(db, data, request)


@router.put("/{id}", dependencies=[Depends(middlewares.verify_user)])
async def update_dataset(
    request: Request,
    id: UUID4,
    data: schemas.DatasourceUpdate,
    db: Session = Depends(get_session),
):
    return ctl.update_dataset(db, id, data, request)


@router.delete("/{id}", dependencies=[Depends(middlewares.verify_user)])
async def delete_dataset(
    request: Request, id: UUID4, db: Session = Depends(get_session)
):
    return ctl.delete_dataset(db, id, request)
