import os
from sqlalchemy.orm import Session
from fastapi import status, Request
from fastapi.responses import JSONResponse

from services_python.data_service.app.models import Datasource
import services_python.data_service.app.schemas as schemas
from services_python.utils.exception import MyException
import services_python.constants.label as label
from services_python.utils.handle_errors_wrapper import handle_database_errors

LIMIT_RECORD = int(os.getenv("LIMIT_RECORD", "50"))


@handle_database_errors
def get_datasets(db: Session, request: Request):
    ALLOWED_FILTER_FIELDS = {"id", "user_id", "type"}
    query_params = dict(request.query_params)

    if request.state.role != label.role["ADMIN"]:
        query_params["user_id"] = request.state.id

    # Lấy giá trị skip và limit từ query_params
    skip = int(query_params.get("skip", 0))
    limit = int(query_params.get("limit", LIMIT_RECORD))

    # Giới hạn giá trị limit trong khoảng từ 0 đến 200
    limit = min(max(int(limit), 0), 200)

    query = db.query(Datasource)
    for field, value in query_params.items():
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


@handle_database_errors
def create_dataset(db: Session, data: schemas.DatasourceCreate, request: Request):
    data.user_id = request.state.id
    new_record = Datasource(**data.dict())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return JSONResponse(
        content={
            "detail": "Tạo datasource thành công.",
            "data": new_record.to_dict(),
        },
        status_code=status.HTTP_201_CREATED,
    )


@handle_database_errors
def update_dataset(
    db: Session, id: int, updated_data: schemas.DatasourceUpdate, request: Request
):
    # Kiểm tra xem datasource tồn tại hay không
    exist_record = db.query(Datasource).filter(Datasource.id == id).first()
    if not exist_record:
        raise MyException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy datasource."
        )

    # Kiểm tra người sở hữu của bản ghi
    if str(exist_record.user_id) != str(request.state.id):
        raise MyException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập vào tài nguyên này.",
        )

    # Chuyển đổi Pydantic model thành từ điển để lặp qua các cặp khóa-giá trị
    updated_data_dict = updated_data.dict()

    # Cập nhật dữ liệu của datasource
    for key, value in updated_data_dict.items():
        setattr(exist_record, key, value)

    # Lưu thay đổi vào cơ sở dữ liệu
    db.commit()
    db.refresh(exist_record)

    return JSONResponse(
        content={
            "detail": "Tạo datasource thành công.",
            "data": exist_record.to_dict(),
        },
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def delete_dataset(db: Session, datasource_id: int, request: Request):
    # Kiểm tra xem datasource tồn tại hay không
    exist_record = db.query(Datasource).filter(Datasource.id == datasource_id).first()
    if not exist_record:
        raise MyException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy datasource."
        )

    # Kiểm tra người sở hữu của bản ghi
    if str(exist_record.user_id) != str(request.state.id):
        raise MyException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập vào tài nguyên này.",
        )

    # Xóa datasource
    db.delete(exist_record)
    db.commit()

    return JSONResponse(
        content={"detail": "Xóa datasource thành công."},
        status_code=status.HTTP_200_OK,
    )
