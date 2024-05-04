import json
from pydantic import UUID4
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile

import services_python.data_service.app.controllers.datamarts as ctl
import services_python.data_service.app.schemas.datamarts as schemas
import services_python.middlewares.auth as middlewares
from services_python.data_service.app.database import get_session

router = APIRouter(prefix="/datamarts", tags=["Datasets"])


@router.get("/", dependencies=[Depends(middlewares.verify_all)])
async def get_datamarts(
    request: Request,
    db: Session = Depends(get_session),
):

    return ctl.get_datamarts(db, request)


@router.get("/query", dependencies=[Depends(middlewares.verify_all)])
async def query_table_datasets(
    request: Request,
    db: Session = Depends(get_session),
):
    return ctl.query_table_datasets(db, request)


@router.post("/", dependencies=[Depends(middlewares.verify_user)])
async def create_dataset(
    request: Request,
    data: schemas.DatasetCreate,
    db: Session = Depends(get_session),
):
    return ctl.create_dataset(
        db,
        data,
        request,
    )


@router.post("/upload_file", dependencies=[Depends(middlewares.verify_user)])
async def create_dataset_upload_file(
    request: Request,
    name: str = Form(...),
    other: str = Form(None),
    file_data: UploadFile = File(...),
    db: Session = Depends(get_session),
):
    # Ép kiểu dữ liệu từ str thành dict
    other_dict = json.loads(other) if other else None

    return ctl.create_dataset_upload_file(
        db,
        file_data,
        schemas.DatasetCreate(name=name, other=other_dict),
        request,
    )


@router.post("/run/{id}", dependencies=[Depends(middlewares.verify_user)])
async def run_dataset(
    request: Request,
    id: UUID4,
    db: Session = Depends(get_session),
):
    return ctl.run_dataset(db, id, request)


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