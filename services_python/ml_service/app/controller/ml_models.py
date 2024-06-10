import os
import requests
import pandas as pd
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

# from services_python.ml_service.app.schemas import ml_models as shemas
from services_python.ml_service.app.models import Project, Run, Model
from services_python.utils.api_response import make_response
from services_python.utils.handle_errors_wrapper import handle_database_errors

headers = {"Content-Type": "application/json"}

# Get environment variables
PREFECT_HOST = os.getenv("PREFECT_HOST")
PREFECT_PORT = os.getenv("PREFECT_PORT")
MLFLOW_HOST = os.getenv("MLFLOW_HOST")
MLFLOW_PORT = os.getenv("MLFLOW_PORT")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")
# Set default limit for records
LIMIT_RECORD = int(os.getenv("LIMIT_RECORD", "50"))


@handle_database_errors
async def search_model(
    request: Request,
    db: Session,
):
    user_id = "00000000-0000-0000-0000-000000000001"

    query_params = dict(request.query_params)

    # Set skip and limit for pagination
    skip = int(query_params.get("skip", 0))
    limit = int(query_params.get("limit", LIMIT_RECORD))
    limit = min(max(int(limit), 0), 200)

    query = (
        db.query(Model)
        .join(Project)
        .filter(Project.user_id == user_id)
        .distinct(Project.id)
        .order_by(Project.id, Model.version.desc())
    )
    total = query.count()
    records = query.offset(skip).limit(limit).all()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=make_response(
            message="Lấy danh sách model thành công",
            data=[record.to_dict() for record in records],
            total=total,
            skip=skip,
            limit=limit,
        ),
    )


@handle_database_errors
async def search_model_version(
    project_id: str,
    request: Request,
    db: Session,
):
    user_id = "00000000-0000-0000-0000-000000000001"
    exist_project = db.query(Project).filter(Project.id == project_id).first()
    if not exist_project:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=make_response(message="Không tìm thấy dự án"),
        )
    if str(exist_project.user_id) != str(user_id):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=make_response(message="Không có quyền truy cập"),
        )

    # Set skip and limit for pagination
    query_params = dict(request.query_params)
    skip = int(query_params.get("skip", 0))
    limit = int(query_params.get("limit", LIMIT_RECORD))
    limit = min(max(int(limit), 0), 200)
    # Query model version
    query = db.query(Model).filter(Model.project_id == project_id)
    # Get total count and records
    total = query.count()
    records = query.offset(skip).limit(limit).all()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=make_response(
            message="Lấy danh sách model version thành công",
            data=[record.to_dict() for record in records],
            total=total,
            skip=skip,
            limit=limit,
        ),
    )


@handle_database_errors
async def get_model_version(
    project_id: str,
    version: str,
    request: Request,
    db: Session,
):
    user_id = "00000000-0000-0000-0000-000000000001"
    exist_project = db.query(Project).filter(Project.id == project_id).first()
    if not exist_project:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=make_response(message="Không tìm thấy dự án"),
        )
    if str(exist_project.user_id) != str(user_id):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=make_response(message="Không có quyền truy cập"),
        )

    if version == "latest":
        exist_version = (
            db.query(Run)
            .join(Model)
            .filter(Run.project_id == project_id)
            .order_by(Model.version.desc())
            .first()
        )
    else:
        exist_version = (
            db.query(Run)
            .join(Model)
            .filter(Run.project_id == project_id, Model.version == version)
            .first()
        )
    if not exist_version:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=make_response(message="Model version không tồn tại"),
        )

    response = requests.get(
        url=f"http://{MLFLOW_HOST}:{MLFLOW_PORT}/api/2.0/mlflow/runs/get",
        headers=headers,
        json={"run_id": exist_version.run_id},
    )

    if 200 <= response.status_code < 300:
        response = response.json()["run"]
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=make_response(
                message="Lấy model version thành công", data=response
            ),
        )
    else:
        return JSONResponse(
            status_code=response.status_code,
            content=make_response(message="Lấy model version thất bại"),
        )
