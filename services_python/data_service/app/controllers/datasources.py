import os
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse

from services_python.data_service.app.models import Datasource
import services_python.data_service.app.schemas as schemas
from services_python.data_service.app.exception import MyException

LIMIT_RECORD = int(os.getenv("LIMIT_RECORD", "50"))


def get_datasources(db: Session, skip: int = 0, limit: int = LIMIT_RECORD, **kwargs):
    ALLOWED_FILTER_FIELDS = {"id", "user_id", "type"}
    query = db.query(Datasource)

    for field, value in kwargs.items():
        if field in ALLOWED_FILTER_FIELDS and value is not None:
            # Lọc theo trường và giá trị tương ứng
            query = query.filter(getattr(Datasource, field) == value)

    datasources = query.offset(skip).limit(limit).all()

    return JSONResponse(
        content={
            "detail": "Lấy danh sách datasource thành công.",
            "skip": skip,
            "limit": limit,
            "total": query.count(),
            "data": [datasource.to_dict() for datasource in datasources],
        },
        status_code=status.HTTP_200_OK,
    )


def create_datasource(db: Session, data: schemas.DatasourceCreate):
    new_datasource = Datasource(**data.dict())
    db.add(new_datasource)
    db.commit()
    db.refresh(new_datasource)

    return JSONResponse(
        content={
            "detail": "Tạo datasource thành công.",
            "data": new_datasource.to_dict(),
        },
        status_code=status.HTTP_201_CREATED,
    )


def update_datasource(
    db: Session, datasource_id: int, updated_data: schemas.DatasourceUpdate
):
    # Kiểm tra xem datasource tồn tại hay không
    existing_datasource = (
        db.query(Datasource).filter(Datasource.id == datasource_id).first()
    )
    if not existing_datasource:
        raise MyException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy datasource."
        )

    # Chuyển đổi Pydantic model thành từ điển để lặp qua các cặp khóa-giá trị
    updated_data_dict = updated_data.dict()

    # Cập nhật dữ liệu của datasource
    for key, value in updated_data_dict.items():
        setattr(existing_datasource, key, value)

    # Lưu thay đổi vào cơ sở dữ liệu
    db.commit()
    db.refresh(existing_datasource)

    return JSONResponse(
        content={
            "detail": "Tạo datasource thành công.",
            "data": existing_datasource.to_dict(),
        },
        status_code=status.HTTP_200_OK,
    )


def delete_datasource(db: Session, datasource_id: int):
    # Kiểm tra xem datasource tồn tại hay không
    existing_datasource = (
        db.query(Datasource).filter(Datasource.id == datasource_id).first()
    )
    if not existing_datasource:
        raise MyException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy datasource."
        )

    # Xóa datasource
    db.delete(existing_datasource)
    db.commit()

    return JSONResponse(
        content={"detail": "Xóa datasource thành công."},
        status_code=status.HTTP_200_OK,
    )
