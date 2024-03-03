import os
from pydantic import UUID4
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from services_python.data_service.app.database import get_session
import services_python.data_service.app.controllers.datasets as ctl
import services_python.data_service.app.schemas as schemas

router = APIRouter(prefix="/datasets", tags=["Datasets"])


@router.get("/")
async def get_datasets(db: Session = Depends(get_session)):
    return ctl.get_datasets(db)


@router.post("/")
async def create_dataset(
    data: schemas.DatasourceCreate, db: Session = Depends(get_session)
):
    return ctl.create_dataset(db, data)


@router.put("/{id}")
async def update_dataset(
    id: UUID4, data: schemas.DatasourceUpdate, db: Session = Depends(get_session)
):
    return ctl.update_dataset(db, id, data)


@router.delete("/{id}")
async def delete_dataset(id: UUID4, db: Session = Depends(get_session)):
    return ctl.delete_dataset(db, id)
