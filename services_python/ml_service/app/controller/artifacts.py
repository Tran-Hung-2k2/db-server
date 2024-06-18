import os
import requests
import pandas as pd
from fastapi import Request, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from services_python.ml_service.app.models import Project, Run, Model
from services_python.utils.api_response import make_response
from services_python.utils.handle_errors_wrapper import handle_database_errors
from services_python.utils.s3 import list_from_s3, read_from_s3

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
async def search_artifact(
    run_id: str,
    request: Request,
    db: Session,
):
    user_id = "00000000-0000-0000-0000-000000000001"
    exist_run = db.query(Run).join(Project).filter(Run.id == run_id).first()
    if not exist_run:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=make_response(message="Run không tồn tại"),
        )
    exist_project = db.query(Project).filter(Project.id == exist_run.project_id).first()
    if str(exist_project.user_id) != user_id:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=make_response(message="Không có quyền truy cập"),
        )

    objects = list_from_s3(
        bucket="mlops", entry=f"{exist_project.experiment_id}/{exist_run.run_id}"
    )
    objects = [
        {"Key": obj["Key"].split("artifacts/")[-1], "Size": obj["Size"]}
        for obj in objects
    ]

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=make_response(
            message="Lấy danh sách artifacts thành công",
            data=objects,
        ),
    )


@handle_database_errors
async def get_artifact(
    run_id: str,
    request: Request,
    db: Session,
):
    user_id = "00000000-0000-0000-0000-000000000001"
    exist_run = db.query(Run).join(Project).filter(Run.id == run_id).first()
    if not exist_run:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=make_response(message="Run không tồn tại"),
        )
    exist_project = db.query(Project).filter(Project.id == exist_run.project_id).first()
    if str(exist_project.user_id) != user_id:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=make_response(message="Không có quyền truy cập"),
        )
    path = request.query_params.get("path")
    # print(f"{exist_project.experiment_id}/{exist_run.run_id}/artifacts/{artifact_path}")
    content = read_from_s3(
        bucket="mlops",
        key=f"{exist_project.experiment_id}/{exist_run.run_id}/artifacts/{path}",
    )
    if path.endswith("png"):
        return Response(
            status_code=status.HTTP_200_OK, content=content, media_type="image/png"
        )
    elif path.endswith("pkl"):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=make_response(
                message="Select a file to preview",
                detail="Supported formats: image, text, html, pdf, geojson files",
            ),
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=make_response(
                message="Lấy artifact thành công", data=content.decode("utf-8")
            ),
        )
