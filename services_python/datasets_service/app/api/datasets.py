import os
import json
from pydantic import UUID4
from sqlalchemy.orm import Session
from services_python.utils.exception import MyException
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile, status
from streaming_form_data import StreamingFormDataParser
from streaming_form_data.targets import FileTarget, ValueTarget
from streaming_form_data.validators import MaxSizeValidator
import streaming_form_data
from starlette.requests import ClientDisconnect

import services_python.datasets_service.app.controllers.datasets as ctl
import services_python.datasets_service.app.schemas.datasets as schemas
import services_python.middlewares.auth as middlewares
from services_python.datasets_service.app.database import get_session

router = APIRouter(prefix="/datasets", tags=["Datasets"])

MAX_FILE_SIZE = 1024 * 1024 * 1024 * 4  # = 4GB
MAX_REQUEST_BODY_SIZE = MAX_FILE_SIZE + 1024


class MaxBodySizeException(Exception):
    def __init__(self, body_len: str):
        self.body_len = body_len


class MaxBodySizeValidator:
    def __init__(self, max_size: int):
        self.body_len = 0
        self.max_size = max_size

    def __call__(self, chunk: bytes):
        self.body_len += len(chunk)
        if self.body_len > self.max_size:
            raise MaxBodySizeException(body_len=self.body_len)


@router.get("/", dependencies=[Depends(middlewares.verify_all)])
async def get_datasets(
    request: Request,
    db: Session = Depends(get_session),
):

    return await ctl.get_datasets(db, request)


@router.get("/query", dependencies=[Depends(middlewares.verify_all)])
async def query_table_datasets(
    request: Request,
    db: Session = Depends(get_session),
):
    return await ctl.query_table_datasets(db, request)


@router.post("/", dependencies=[Depends(middlewares.verify_user)])
async def create_dataset_upload_file(
    request: Request,
    db: Session = Depends(get_session),
):
    body_validator = MaxBodySizeValidator(MAX_REQUEST_BODY_SIZE)
    filename = request.headers.get("Filename")

    if not filename:
        raise MyException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Thiếu tiêu đề 'Filename'.",
        )
    try:
        filepath = os.path.join("./temp/", os.path.basename(filename))
        file_ = FileTarget(filepath, validator=MaxSizeValidator(MAX_FILE_SIZE))
        name = ValueTarget()
        description = ValueTarget()
        parser = StreamingFormDataParser(headers=request.headers)
        parser.register("file", file_)
        parser.register("name", name)
        parser.register("description", description)

        async for chunk in request.stream():
            body_validator(chunk)
            parser.data_received(chunk)
    except ClientDisconnect:
        print("Khách hàng đã ngắt kết nối.")
    except MaxBodySizeException as e:
        raise MyException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Vượt quá giới hạn kích thước yêu cầu tối đa ({MAX_REQUEST_BODY_SIZE} bytes) ({e.body_len} bytes đã đọc).",
        )
    except streaming_form_data.validators.ValidationError:
        raise MyException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Vượt quá giới hạn kích thước tệp tối đa ({MAX_FILE_SIZE} bytes).",
        )
    except Exception as e:
        raise MyException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Có lỗi xảy ra khi tải lên tệp. Chi tiết: " + str(e),
        )

    if not name.value:
        raise MyException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Tên tập dữ liệu không được bỏ trống.",
        )
    if not file_.multipart_filename:
        raise MyException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Thiếu tệp dữ liệu.",
        )

    return await ctl.create_dataset(
        db,
        filepath,  # Thay file_data bằng đường dẫn tệp đã tải lên
        schemas.DatasetCreate(
            name=name.value.decode(), description=description.value.decode()
        ),
        request,
    )


@router.post("/run/{id}", dependencies=[Depends(middlewares.verify_user)])
async def run_dataset(
    request: Request,
    id: UUID4,
    db: Session = Depends(get_session),
):
    return await ctl.run_dataset(db, id, request)


@router.patch("/{id}", dependencies=[Depends(middlewares.verify_user)])
async def update_dataset(
    request: Request,
    id: UUID4,
    data: schemas.DatasetUpdate,
    db: Session = Depends(get_session),
):
    return await ctl.update_dataset(db, id, data, request)


@router.delete("/{id}", dependencies=[Depends(middlewares.verify_user)])
async def delete_dataset(
    request: Request, id: UUID4, db: Session = Depends(get_session)
):
    return await ctl.delete_dataset(db, id, request)
