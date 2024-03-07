import os
from sqlalchemy.orm import Session
from fastapi import status, Request
from fastapi.responses import JSONResponse

from services_python.data_service.app.models import DatasourceType
import services_python.data_service.app.schemas.datasource_types as schemas
from services_python.utils.exception import MyException
import services_python.constants.label as label
from services_python.utils.handle_errors_wrapper import handle_database_errors

LIMIT_RECORD = int(os.getenv("LIMIT_RECORD", "50"))


@handle_database_errors
def get_datasource_types(db: Session, request: Request):
    ALLOWED_FILTER_FIELDS = {"id"}
    query_params = dict(request.query_params)

    # Lấy giá trị skip và limit từ query_params
    skip = int(query_params.get("skip", 0))
    limit = int(query_params.get("limit", LIMIT_RECORD))

    # Giới hạn giá trị limit trong khoảng từ 0 đến 200
    limit = min(max(int(limit), 0), 200)

    query = db.query(DatasourceType)
    for field, value in query_params.items():
        if field in ALLOWED_FILTER_FIELDS and value is not None:
            # Lọc theo trường và giá trị tương ứng
            query = query.filter(getattr(DatasourceType, field) == value)

    records = query.offset(skip).limit(limit).all()

    return JSONResponse(
        content={
            "detail": "Lấy danh sách datasource type thành công.",
            "skip": skip,
            "limit": limit,
            "total": query.count(),
            "data": [record.to_dict() for record in records],
        },
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def create_datasource_type(db: Session, data: schemas.DatasourceTypeCreate):
    # Kiểm tra xem record tồn tại hay không
    exist_record = (
        db.query(DatasourceType).filter(DatasourceType.name == data.name).first()
    )
    if exist_record:
        raise MyException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Datasource type với tên này đã tồn tại.",
        )
    new_record = DatasourceType(**data.dict())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return JSONResponse(
        content={
            "detail": "Tạo datasource type thành công.",
            "data": new_record.to_dict(),
        },
        status_code=status.HTTP_201_CREATED,
    )


@handle_database_errors
def update_datasource_type(
    db: Session, id: int, updated_data: schemas.DatasourceTypeUpdate
):
    # Kiểm tra xem record tồn tại hay không
    exist_record = db.query(DatasourceType).filter(DatasourceType.id == id).first()
    if not exist_record:
        raise MyException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy datasource type.",
        )

    # Chuyển đổi Pydantic model thành từ điển để lặp qua các cặp khóa-giá trị
    updated_data_dict = updated_data.dict()

    # Cập nhật dữ liệu
    for key, value in updated_data_dict.items():
        setattr(exist_record, key, value)

    # Lưu thay đổi vào cơ sở dữ liệu
    db.commit()
    db.refresh(exist_record)

    return JSONResponse(
        content={
            "detail": "Cập nhật datasource type thành công.",
            "data": exist_record.to_dict(),
        },
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def delete_datasource_type(db: Session, id: int):
    exist_record = db.query(DatasourceType).filter(DatasourceType.id == id).first()
    if not exist_record:
        raise MyException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy datasource type.",
        )

    db.delete(exist_record)
    db.commit()

    return JSONResponse(
        content={"detail": "Xóa datasource type thành công."},
        status_code=status.HTTP_200_OK,
    )
