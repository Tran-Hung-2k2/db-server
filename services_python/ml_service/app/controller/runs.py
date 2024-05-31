import os
import requests
from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from services_python.ml_service.app import schemas
from services_python.ml_service.app.models import Run, Project
from services_python.utils import (
    save_to_s3,
    handle_database_errors,
    make_response,
    name_generator,
)

headers = {"Content-Type": "application/json"}

# Get environment variables
PREFECT_HOST = os.getenv("PREFECT_HOST")
PREFECT_PORT = os.getenv("PREFECT_PORT")
MLFLOW_HOST = os.getenv("MLFLOW_HOST")
MLFLOW_PORT = os.getenv("MLFLOW_PORT")
AWS_ACCESS_KEY_ID = os.getenv("MINIO_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("MINIO_SECRET_ACCESS_KEY")
AWS_ENDPOINT_URL = os.getenv("MINIO_ENDPOINT_URL")
# os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
# os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
# os.environ["AWS_ENDPOINT_URL"] = AWS_ENDPOINT_URL

# Set default limit for records
LIMIT_RECORD = int(os.getenv("LIMIT_RECORD", "50"))


@handle_database_errors
async def create_run(
    db: Session,
    request: Request,
    project_id: str,
    data: schemas.RunCreate,
):
    exist_project = db.query(Project).filter(Project.id == project_id).first()
    if not exist_project:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=make_response(message="Không tìm thấy dự án"),
        )
    data.project_id = project_id
    # Check deployment_id
    deployment_id = exist_project.deployment_id
    if not deployment_id:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=make_response(message="Dự án chưa cấu hình"),
        )
    if not data.name:
        data.name = name_generator()

    new_run = Run(**data.dict())
    db.add(new_run)
    db.flush()

    request_payload = data.config
    request_payload["name"] = str(new_run.id)
    request_payload["parameters"] = {"run_name": str(new_run.id)}
    # Create flow run from deployment
    response = requests.post(
        url=f"http://{PREFECT_HOST}:{PREFECT_PORT}/api/deployments/{deployment_id}/create_flow_run",
        headers=headers,
        json=request_payload,
    )
    if 400 <= response.status_code < 500:
        db.rollback()
        return JSONResponse(
            status_code=response.status_code,
            content=make_response(
                message="Khởi chạy dự án thất bại", detail=response.json()
            ),
        )
    else:
        data.flow_run_id = response.json()["id"]
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=make_response(
                message="Khởi chạy dự án thành công",
            ),
        )
