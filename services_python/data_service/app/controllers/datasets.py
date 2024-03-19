import os
from sqlalchemy.orm import Session
from fastapi import status, Request, UploadFile
from fastapi.responses import JSONResponse

from services_python.data_service.app.models import Dataset, Datasource
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
    ALLOWED_FILTER_FIELDS = {"id", "datasource_id", "user_id"}
    query_params = dict(request.query_params)

    if request.state.role != label.role["ADMIN"]:
        # Nếu không phải là ADMIN, thêm điều kiện để chỉ lấy datasets thuộc về user_id
        query_params["user_id"] = str(request.state.id)

    # Lấy giá trị skip và limit từ query_params
    skip = int(query_params.get("skip", 0))
    limit = int(query_params.get("limit", LIMIT_RECORD))

    # Giới hạn giá trị limit trong khoảng từ 0 đến 200
    limit = min(max(int(limit), 0), 200)

    query = db.query(Dataset)
    query = query.join(Datasource)
    for field, value in query_params.items():
        if field in ALLOWED_FILTER_FIELDS and value is not None:
            # Lọc theo trường và giá trị tương ứng
            # Nếu là user_id, thì lọc trong bảng Datasource
            if field == "user_id":
                query = query.filter(Datasource.user_id == value)
            else:
                # Ngược lại, lọc trong bảng dataset
                query = query.filter(getattr(Dataset, field) == value)

    records = query.offset(skip).limit(limit).all()

    return JSONResponse(
        content={
            "detail": "Lấy danh sách dataset thành công.",
            "skip": skip,
            "limit": limit,
            "total": query.count(),
            "data": [record.to_dict() for record in records],
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
                status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy dataset."
            )

        # Kiểm tra xem datasource tồn tại hay không
        exist_datasource = (
            db.query(Datasource)
            .filter(Datasource.id == exist_dataset.datasource_id)
            .first()
        )

        if not exist_datasource:
            raise MyException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy datasource.",
            )

        # Kiểm tra người sở hữu của bản ghi
        if str(exist_datasource.user_id) != str(request.state.id):
            raise MyException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền truy cập vào tài nguyên này.",
            )

    records, total = query_sql_from_delta_table(
        user_id, dataset_id, exist_dataset.name, sql_cmd, skip, limit
    )

    return JSONResponse(
        content={
            "detail": "Truy vấn danh dataset thành công.",
            "skip": skip,
            "limit": limit,
            "total": total,
            "data": records,
        },
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def create_dataset(db: Session, data: schemas.DatasetCreate, request: Request):
    # Kiểm tra xem datasource tồn tại hay không
    exist_datasource = (
        db.query(Datasource).filter(Datasource.id == data.datasource_id).first()
    )
    if not exist_datasource:
        raise MyException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy datasource."
        )

    # Kiểm tra người sở hữu của bản ghi
    if str(exist_datasource.user_id) != str(request.state.id):
        raise MyException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập vào tài nguyên này.",
        )

    if (
        exist_datasource.datasource_type.name
        == label.datasource_type_name["UPLOAD_FILE"]
    ):
        raise MyException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Datasource type không phù hợp.",
        )

    new_record = Dataset(**data.dict())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return JSONResponse(
        content={
            "detail": "Tạo dataset thành công.",
            "data": new_record.to_dict(),
        },
        status_code=status.HTTP_201_CREATED,
    )


@handle_database_errors
def create_dataset_upload_file(
    db: Session, file_data: UploadFile, data: schemas.DatasetCreate, request: Request
):
    # Kiểm tra xem datasource tồn tại hay không
    exist_datasource = (
        db.query(Datasource).filter(Datasource.id == data.datasource_id).first()
    )
    if not exist_datasource:
        raise MyException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy datasource."
        )

    # Kiểm tra người sở hữu của bản ghi
    if str(exist_datasource.user_id) != str(request.state.id):
        raise MyException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập vào tài nguyên này.",
        )

    if (
        exist_datasource.datasource_type.name
        != label.datasource_type_name["UPLOAD_FILE"]
    ):
        raise MyException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Datasource type không phù hợp.",
        )

    new_record = Dataset(**data.dict())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    save_file_to_s3_as_delta(file_data, request.state.id, new_record.id)

    return JSONResponse(
        content={
            "detail": "Tạo dataset thành công.",
            "data": new_record.to_dict(),
        },
        status_code=status.HTTP_201_CREATED,
    )


@handle_database_errors
def run_dataset(db: Session, id: int, request: Request):
    # Kiểm tra xem dataset tồn tại hay không
    exist_dataset = db.query(Dataset).filter(Dataset.id == id).first()
    if not exist_dataset:
        raise MyException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy dataset."
        )

    # Kiểm tra xem datasource tồn tại hay không
    exist_datasource = (
        db.query(Datasource)
        .filter(Datasource.id == exist_dataset.datasource_id)
        .first()
    )
    if not exist_datasource:
        raise MyException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy datasource."
        )

    # Kiểm tra người sở hữu của bản ghi
    if str(exist_datasource.user_id) != str(request.state.id):
        raise MyException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập vào tài nguyên này.",
        )

    return JSONResponse(
        content={
            "detail": "Cập nhật dataset thành công.",
            "data": exist_dataset.to_dict(),
        },
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def update_dataset(
    db: Session, id: int, updated_data: schemas.DatasetUpdate, request: Request
):
    # Kiểm tra xem dataset tồn tại hay không
    exist_dataset = db.query(Dataset).filter(Dataset.id == id).first()
    if not exist_dataset:
        raise MyException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy dataset."
        )

    # Kiểm tra xem datasource tồn tại hay không
    exist_datasource = (
        db.query(Datasource)
        .filter(Datasource.id == exist_dataset.datasource_id)
        .first()
    )
    if not exist_datasource:
        raise MyException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy datasource."
        )

    # Kiểm tra người sở hữu của bản ghi
    if str(exist_datasource.user_id) != str(request.state.id):
        raise MyException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập vào tài nguyên này.",
        )

    # Chuyển đổi Pydantic model thành từ điển để lặp qua các cặp khóa-giá trị
    updated_data_dict = updated_data.dict()

    # Cập nhật dữ liệu của datasource
    for key, value in updated_data_dict.items():
        setattr(exist_dataset, key, value)

    # Lưu thay đổi vào cơ sở dữ liệu
    db.commit()
    db.refresh(exist_dataset)

    return JSONResponse(
        content={
            "detail": "Cập nhật dataset thành công.",
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
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy dataset."
        )

    # Kiểm tra xem datasource tồn tại hay không
    exist_datasource = (
        db.query(Datasource)
        .filter(Datasource.id == exist_dataset.datasource_id)
        .first()
    )
    if not exist_datasource:
        raise MyException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy datasource."
        )

    # Kiểm tra người sở hữu của bản ghi
    if str(exist_datasource.user_id) != str(request.state.id):
        raise MyException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập vào tài nguyên này.",
        )

    # Xóa datasource
    db.delete(exist_dataset)
    db.commit()

    return JSONResponse(
        content={"detail": "Xóa dataset thành công."},
        status_code=status.HTTP_200_OK,
    )
