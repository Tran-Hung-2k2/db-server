import os
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from fastapi import status, Request, UploadFile
from fastapi.responses import JSONResponse

from services_python.data_service.app.models import Dataset
import services_python.data_service.app.schemas.datasets as schemas
from services_python.utils.exception import MyException
import services_python.constants.label as label
from services_python.utils.handle_errors_wrapper import handle_database_errors
from services_python.utils.delta import (
    save_file_to_s3_as_delta,
    query_sql_from_delta_table,
)

LIMIT_RECORD = int(os.getenv("LIMIT_RECORD", "50"))


@handle_database_errors
def get_datasets(db: Session, request: Request):
    ALLOWED_FILTER_FIELDS = {"id", "user_id"}
    query_params = dict(request.query_params)

    if request.state.role != label.role["ADMIN"]:
        # Nếu không phải là ADMIN, thêm điều kiện để chỉ lấy datasets thuộc về user_id
        query_params["user_id"] = str(request.state.id)

    # Lấy giá trị skip và limit từ query_params
    skip = int(query_params.get("skip", 0))
    limit = int(query_params.get("limit", LIMIT_RECORD))
    sort_by = query_params.get("sort_by", "created_at")
    sort_dim = query_params.get("sort_dim", "desc")
    name = query_params.get("name", "")

    # Giới hạn giá trị limit trong khoảng từ 0 đến 200
    limit = min(max(int(limit), 0), 200)

    query = db.query(Dataset)

    # Tìm kiếm theo tên
    if name:
        query = query.filter(Dataset.name.ilike(f"%{name}%"))

    for field, value in query_params.items():
        if field in ALLOWED_FILTER_FIELDS and value is not None:
            # Lọc theo trường và giá trị tương ứng
            query = query.filter(getattr(Dataset, field) == value)

    # Sắp xếp kết quả truy vấn
    if sort_dim.lower() == "asc":
        query = query.order_by(asc(getattr(Dataset, sort_by)))
    else:
        query = query.order_by(desc(getattr(Dataset, sort_by)))

    total = query.count()
    records = query.offset(skip).limit(limit).all()

    return JSONResponse(
        content={
            "message": "Lấy danh sách tập dữ liệu thành công.",
            "data": [record.to_dict() for record in records],
            "skip": skip,
            "limit": limit,
            "total": total,
        },
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def query_table_datasets(db: Session, request: Request):
    query_params = dict(request.query_params)
    user_id = request.state.id
    dataset_id = query_params.get("dataset_id")
    sql_cmd = query_params.get("sql_cmd")
    skip = int(query_params.get("skip", 0))
    limit = int(query_params.get("limit", LIMIT_RECORD))

    # Giới hạn giá trị limit trong khoảng từ 0 đến 200
    limit = min(max(int(limit), 0), 200)

    if request.state.role != label.role["ADMIN"]:
        # Kiểm tra xem dataset tồn tại hay không
        exist_dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not exist_dataset:
            raise MyException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy tập dữ liệu.",
            )

        # Kiểm tra người sở hữu của bản ghi
        if str(exist_dataset.user_id) != str(request.state.id):
            raise MyException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền truy cập vào tài nguyên này.",
            )

    records, total = query_sql_from_delta_table(
        user_id, dataset_id, exist_dataset.name, sql_cmd, skip, limit
    )

    return JSONResponse(
        content={
            "message": "Truy vấn danh tập dữ liệu thành công.",
            "skip": skip,
            "limit": limit,
            "total": total,
            "data": records,
        },
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def create_dataset(db: Session, data: schemas.DatasetCreate, request: Request):
    data.user_id = request.state.id
    new_record = Dataset(**data.dict())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return JSONResponse(
        content={
            "message": "Tạo tập dữ liệu thành công.",
            "detail": "",
            "data": new_record.to_dict(),
        },
        status_code=status.HTTP_201_CREATED,
    )


@handle_database_errors
def create_dataset_upload_file(
    db: Session, file_data: UploadFile, data: schemas.DatasetCreate, request: Request
):
    data.user_id = request.state.id
    new_record = Dataset(**data.dict())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    save_file_to_s3_as_delta(file_data, request.state.id, new_record.id)

    return JSONResponse(
        content={
            "message": "Tạo tập dữ liệu thành công.",
            "detail": "",
            "data": new_record.to_dict(),
        },
        status_code=status.HTTP_201_CREATED,
    )


@handle_database_errors
def update_dataset(
    db: Session, id: int, updated_data: schemas.DatasetUpdate, request: Request
):
    # Kiểm tra xem dataset tồn tại hay không
    exist_dataset = db.query(Dataset).filter(Dataset.id == id).first()
    if not exist_dataset:
        raise MyException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tập dữ liệu."
        )

    # Kiểm tra người sở hữu của bản ghi
    if str(exist_dataset.user_id) != str(request.state.id):
        raise MyException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập vào tài nguyên này.",
        )

    # Chuyển đổi Pydantic model thành từ điển để lặp qua các cặp khóa-giá trị
    updated_data_dict = updated_data.dict()

    # Cập nhật dữ liệu
    for key, value in updated_data_dict.items():
        setattr(exist_dataset, key, value)

    # Lưu thay đổi vào cơ sở dữ liệu
    db.commit()
    db.refresh(exist_dataset)

    return JSONResponse(
        content={
            "message": "Cập nhật tập dữ liệu thành công.",
            "detail": "",
            "data": exist_dataset.to_dict(),
        },
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def delete_dataset(db: Session, id: int, request: Request):
    # Kiểm tra xem dataset tồn tại hay không
    exist_dataset = db.query(Dataset).filter(Dataset.id == id).first()
    if not exist_dataset:
        raise MyException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tập dữ liệu."
        )

    # Kiểm tra người sở hữu của bản ghi
    if str(exist_dataset.user_id) != str(request.state.id):
        raise MyException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập vào tài nguyên này.",
        )

    # Xóa dataset
    db.delete(exist_dataset)
    db.commit()

    return JSONResponse(
        content={"message": "Xóa tập dữ liệu thành công."},
        status_code=status.HTTP_200_OK,
    )
