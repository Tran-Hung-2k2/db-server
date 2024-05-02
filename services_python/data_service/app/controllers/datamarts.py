import os
from sqlalchemy.orm import Session
from fastapi import status, Request, UploadFile
from fastapi.responses import JSONResponse

from services_python.data_service.app.models import Datamart
import services_python.data_service.app.schemas.datamarts as schemas
from services_python.utils.exception import MyException
import services_python.constants.label as label
from services_python.utils.handle_errors_wrapper import handle_database_errors
from services_python.utils.delta import (
    save_file_to_s3_as_delta,
    query_sql_from_delta_table,
)

LIMIT_RECORD = int(os.getenv("LIMIT_RECORD", "50"))


@handle_database_errors
def get_datamarts(db: Session, request: Request):
    ALLOWED_FILTER_FIELDS = {"id", "user_id"}
    query_params = dict(request.query_params)

    if request.state.role != label.role["ADMIN"]:
        # Nếu không phải là ADMIN, thêm điều kiện để chỉ lấy datamarts thuộc về user_id
        query_params["user_id"] = str(request.state.id)

    # Lấy giá trị skip và limit từ query_params
    skip = int(query_params.get("skip", 0))
    limit = int(query_params.get("limit", LIMIT_RECORD))

    # Giới hạn giá trị limit trong khoảng từ 0 đến 200
    limit = min(max(int(limit), 0), 200)

    query = db.query(Datamart)

    for field, value in query_params.items():
        if field in ALLOWED_FILTER_FIELDS and value is not None:
            # Lọc theo trường và giá trị tương ứng
            query = query.filter(getattr(Datamart, field) == value)

    total = query.count()
    records = query.offset(skip).limit(limit).all()

    return JSONResponse(
        content={
            "detail": "Lấy danh sách datamart thành công.",
            "skip": skip,
            "limit": limit,
            "total": total,
            "data": [record.to_dict() for record in records],
        },
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def query_table_datamarts(db: Session, request: Request):
    query_params = dict(request.query_params)
    user_id = request.state.id
    datamart_id = query_params.get("datamart_id")
    sql_cmd = query_params.get("sql_cmd")
    skip = int(query_params.get("skip", 0))
    limit = int(query_params.get("limit", LIMIT_RECORD))

    # Giới hạn giá trị limit trong khoảng từ 0 đến 200
    limit = min(max(int(limit), 0), 200)

    if request.state.role != label.role["ADMIN"]:
        # Kiểm tra xem datamart tồn tại hay không
        exist_datamart = db.query(Datamart).filter(Datamart.id == datamart_id).first()
        if not exist_datamart:
            raise MyException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy datamart."
            )

        # Kiểm tra người sở hữu của bản ghi
        if str(exist_datamart.user_id) != str(request.state.id):
            raise MyException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền truy cập vào tài nguyên này.",
            )

    records, total = query_sql_from_delta_table(
        user_id, datamart_id, exist_datamart.name, sql_cmd, skip, limit
    )

    return JSONResponse(
        content={
            "detail": "Truy vấn danh datamart thành công.",
            "skip": skip,
            "limit": limit,
            "total": total,
            "data": records,
        },
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def create_datamart(db: Session, data: schemas.DatamartCreate, request: Request):
    data.user_id = request.state.id
    new_record = Datamart(**data.dict())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return JSONResponse(
        content={
            "detail": "Tạo datamart thành công.",
            "data": new_record.to_dict(),
        },
        status_code=status.HTTP_201_CREATED,
    )


@handle_database_errors
def create_datamart_upload_file(
    db: Session, file_data: UploadFile, data: schemas.DatamartCreate, request: Request
):
    data.user_id = request.state.id
    new_record = Datamart(**data.dict())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    save_file_to_s3_as_delta(file_data, request.state.id, new_record.id)

    return JSONResponse(
        content={
            "detail": "Tạo datamart thành công.",
            "data": new_record.to_dict(),
        },
        status_code=status.HTTP_201_CREATED,
    )


@handle_database_errors
def update_datamart(
    db: Session, id: int, updated_data: schemas.DatamartUpdate, request: Request
):
    # Kiểm tra xem datamart tồn tại hay không
    exist_datamart = db.query(Datamart).filter(Datamart.id == id).first()
    if not exist_datamart:
        raise MyException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy datamart."
        )

    # Kiểm tra người sở hữu của bản ghi
    if str(exist_datamart.user_id) != str(request.state.id):
        raise MyException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập vào tài nguyên này.",
        )

    # Chuyển đổi Pydantic model thành từ điển để lặp qua các cặp khóa-giá trị
    updated_data_dict = updated_data.dict()

    # Cập nhật dữ liệu
    for key, value in updated_data_dict.items():
        setattr(exist_datamart, key, value)

    # Lưu thay đổi vào cơ sở dữ liệu
    db.commit()
    db.refresh(exist_datamart)

    return JSONResponse(
        content={
            "detail": "Cập nhật datamart thành công.",
            "data": exist_datamart.to_dict(),
        },
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def delete_datamart(db: Session, id: int, request: Request):
    # Kiểm tra xem datamart tồn tại hay không
    exist_datamart = db.query(Datamart).filter(Datamart.id == id).first()
    if not exist_datamart:
        raise MyException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy datamart."
        )

    # Kiểm tra người sở hữu của bản ghi
    if str(exist_datamart.user_id) != str(request.state.id):
        raise MyException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập vào tài nguyên này.",
        )

    # Xóa datamart
    db.delete(exist_datamart)
    db.commit()

    return JSONResponse(
        content={"detail": "Xóa datamart thành công."},
        status_code=status.HTTP_200_OK,
    )
