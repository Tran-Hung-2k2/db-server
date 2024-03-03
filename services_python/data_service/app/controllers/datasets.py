from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from services_python.data_service.app.models import Datasource
import services_python.data_service.app.schemas as schemas


def get_datasets(db: Session, skip: int, limit: int):
    datasources = db.query(Datasource).offset(skip).limit(limit).all()
    return JSONResponse(
        content={
            "detail": "Lấy danh sách datasource thành công.",
            "data": [datasource.to_dict() for datasource in datasources],
        },
        status_code=200,
    )


def create_dataset(db: Session, data: schemas.DatasourceCreate):
    new_dataset = Datasource(**data.dict())
    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)

    return JSONResponse(
        content={
            "detail": "Tạo datasource thành công.",
            "data": new_dataset.to_dict(),
        },
        status_code=201,
    )


def update_dataset(
    db: Session, datasource_id: int, updated_data: schemas.DatasourceUpdate
):
    # Kiểm tra xem datasource tồn tại hay không
    existing_dataset = (
        db.query(Datasource).filter(Datasource.id == datasource_id).first()
    )
    if not existing_dataset:
        raise HTTPException(status_code=404, detail="Không tìm thấy datasource.")

    # Chuyển đổi Pydantic model thành từ điển để lặp qua các cặp khóa-giá trị
    updated_data_dict = updated_data.dict()

    # Cập nhật dữ liệu của datasource
    for key, value in updated_data_dict.items():
        setattr(existing_dataset, key, value)

    # Lưu thay đổi vào cơ sở dữ liệu
    db.commit()
    db.refresh(existing_dataset)

    return JSONResponse(
        content={
            "detail": "Tạo datasource thành công.",
            "data": existing_dataset.to_dict(),
        },
        status_code=200,
    )


def delete_dataset(db: Session, datasource_id: int):
    # Kiểm tra xem datasource tồn tại hay không
    existing_dataset = (
        db.query(Datasource).filter(Datasource.id == datasource_id).first()
    )
    if not existing_dataset:
        raise HTTPException(status_code=404, detail="Không tìm thấy datasource.")

    # Xóa datasource
    db.delete(existing_dataset)
    db.commit()

    return JSONResponse(
        content={"detail": "Xóa datasource thành công."},
        status_code=200,
    )
