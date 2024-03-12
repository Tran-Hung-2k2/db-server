from sqlalchemy.orm import Session
from fastapi import APIRouter, UploadFile, Request, Depends, Form, File
from pydantic import UUID4

from services_python.data_service.app.database import get_session
import services_python.data_service.app.controllers.datasets as ctl
import services_python.data_service.app.schemas.datasets as schemas
import services_python.middlewares.auth as middlewares

router = APIRouter(prefix="/datasets", tags=["Datasets"])


@router.get("/", dependencies=[Depends(middlewares.verify_all)])
async def get_datasets(
    request: Request,
    db: Session = Depends(get_session),
):
    return ctl.get_datasets(db, request)


@router.get("/query", dependencies=[Depends(middlewares.verify_all)])
async def query_table_datasets(
    request: Request,
    db: Session = Depends(get_session),
):
    return ctl.query_table_datasets(db, request)


@router.post("/upload_file", dependencies=[Depends(middlewares.verify_user)])
async def create_dataset_upload_file(
    request: Request,
    datasource_id: str = Form(...),
    name: str = Form(...),
    other: str = Form(None),
    file_data: UploadFile = File(...),
    db: Session = Depends(get_session),
):
    return ctl.create_dataset_upload_file(
        db,
        file_data,
        schemas.DatasetCreate(datasource_id=datasource_id, name=name, other=other),
        request,
    )


@router.put("/{id}", dependencies=[Depends(middlewares.verify_user)])
async def update_dataset(
    request: Request,
    id: UUID4,
    data: schemas.DatasetUpdate,
    db: Session = Depends(get_session),
):
    return ctl.update_dataset(db, id, data, request)


@router.delete("/{id}", dependencies=[Depends(middlewares.verify_user)])
async def delete_dataset(
    request: Request, id: UUID4, db: Session = Depends(get_session)
):
    return ctl.delete_dataset(db, id, request)
