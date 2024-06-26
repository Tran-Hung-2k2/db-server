import os
import requests
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from services_python.ml_service.app.constants.sklearn import SKLEARN_CONFIG
from services_python.ml_service.app.schemas import projects as schemas
from services_python.ml_service.app.models import Project, Run
from services_python.utils.s3 import save_to_s3
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
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASS")
DB_NAME = os.getenv("POSTGRES_NAME")
SKLEARN_FLOW_ID = os.getenv("SKLEARN_FLOW_ID")
PYTORCH_FLOW_ID = os.getenv("PYTORCH_FLOW_ID")
# Set default limit for records
LIMIT_RECORD = int(os.getenv("LIMIT_RECORD", "50"))


@handle_database_errors
async def create_project(
    data: schemas.ProjectCreate,
    request: Request,
    db: Session,
):
    # Set user_id and name_dev
    data.user_id = "00000000-0000-0000-0000-000000000001"

    # Check if project already exists
    exist_project = (
        db.query(Project)
        .filter(Project.name == data.name, Project.user_id == data.user_id)
        .first()
    )
    if exist_project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=make_response(message="Tên dự án đã tồn tại"),
        )
    new_project = Project(**data.dict())
    db.add(new_project)
    db.flush()
    db.refresh(new_project)
    # Create experiment in MLflow
    response = requests.post(
        url=f"http://{MLFLOW_HOST}:{MLFLOW_PORT}/api/2.0/mlflow/experiments/create",
        headers=headers,
        json={"name": f"{new_project.id}"},
    )
    if 200 <= response.status_code < 300:
        new_project.experiment_id = response.json()["experiment_id"]
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=make_response(message="Tạo dự án thành công"),
        )
    else:
        db.rollback()
        return JSONResponse(
            status_code=response.status_code,
            content=make_response(message="Tạo dự án thất bại"),
        )


@handle_database_errors
async def search_project(
    request: Request,
    db: Session,
):
    user_id = "00000000-0000-0000-0000-000000000001"
    query_params = dict(request.query_params)
    query_params["user_id"] = user_id
    # Set skip and limit for pagination
    skip = int(query_params.get("skip", 0))
    limit = int(query_params.get("limit", LIMIT_RECORD))
    limit = min(max(int(limit), 0), 200)

    query = db.query(
        Project.id,
        Project.name,
        Project.description,
        Project.created_at,
        Project.updated_at,
    ).filter(Project.user_id == user_id)

    # Get total count and records
    total = query.count()
    records = query.offset(skip).limit(limit).all()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=make_response(
            message="Lấy danh sách dự án thành công",
            data=jsonable_encoder([record._asdict() for record in records]),
            total=total,
            skip=skip,
            limit=limit,
        ),
    )


@handle_database_errors
async def delete_project(
    id: str,
    request: Request,
    db: Session,
):
    user_id = "00000000-0000-0000-0000-000000000000"
    exist_project = db.query(Project).filter(Project.id == id).first()
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

    # Delete project
    db.delete(exist_project)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=make_response(message="Xóa dự án thành công"),
    )


@handle_database_errors
async def update_project(
    id: str,
    data: schemas.ProjectUpdate,
    request: Request,
    db: Session,
):
    user_id = "00000000-0000-0000-0000-000000000000"
    exist_project = db.query(Project).filter(Project.id == id).first()
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
    # Update project data
    for key, value in data.dict().items():
        setattr(exist_project, key, value)

    # Save changes to the database
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Cập nhật dự án thành công"},
    )


@handle_database_errors
async def get_config(
    request: Request,
    db: Session,
):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=make_response(
            message="Lấy cấu hình dự án thành công", data=SKLEARN_CONFIG
        ),
    )


@handle_database_errors
async def config_project(
    id: str,
    data: schemas.ProjectConfig,
    request: Request,
    db: Session,
):
    user_id = "00000000-0000-0000-0000-000000000000"
    exist_project = db.query(Project).filter(Project.id == id).first()
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
    # Save flow content to Minio S3
    if data.flow == "sklearnflow":
        from services_python.ml_service.app.templates.sklearn_flow import (
            SKLEARN_FLOW as FLOW,
        )

        flow_id = SKLEARN_FLOW_ID
    elif data.flow == "pytorchflow":
        from services_python.ml_service.app.templates.pytorch_flow import (
            PYTORCH_FLOW as FLOW,
        )

        flow_id = PYTORCH_FLOW_ID

    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=make_response("Cấu hình dự án không hợp lệ"),
        )
    entry = f"{exist_project.id}.py"
    save_to_s3(
        bucket="mlops",
        entry=entry,
        content=FLOW.replace("{{ flow }}", data.flow)
        .replace("{{ name }}", f"{exist_project.id}")
        .replace("{{ task }}", data.config["task"])
        .replace("{{ dataset }}", data.config["dataset"])
        .replace("{{ lib }}", data.config["lib"])
        .replace("{{ model }}", data.config["model"])
        .replace("{{ metric }}", data.config["metric"]),
    )
    # Deploy flow to work pool
    response = requests.post(
        url=f"http://{PREFECT_HOST}:{PREFECT_PORT}/api/deployments/",
        headers=headers,
        json={
            "name": f"{exist_project.id}",
            "flow_id": flow_id,
            "entrypoint": f"{entry}:{data.flow}",
            "work_pool_name": "Process",
            "job_variables": {
                "env": {
                    "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
                    "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
                    "AWS_ENDPOINT_URL": AWS_ENDPOINT_URL,
                    "MLFLOW_HOST": MLFLOW_HOST,
                    "MLFLOW_PORT": MLFLOW_PORT,
                    "DB_HOST": DB_HOST,
                    "DB_PORT": DB_PORT,
                    "DB_USER": DB_USER,
                    "DB_PASS": DB_PASS,
                    "DB_NAME": DB_NAME,
                }
            },
            "pull_steps": [
                {
                    "prefect.deployments.steps.pull_from_remote_storage": {
                        "url": f"s3://mlops/",
                        "requires": "s3fs",
                    }
                }
            ],
            "schedules": [],
        },
    )
    if 200 <= response.status_code < 300:
        data.deployment_id = response.json()["id"]
        # Update project data
        for key, value in data.dict().items():
            setattr(exist_project, key, value)
        # Save changes to the database
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=make_response(message="Cấu hình dự án thành công"),
        )
    else:
        return JSONResponse(
            status_code=response.status_code,
            content=make_response(
                message="Cấu hình dự án thất bại", detail=response.json()
            ),
        )


@handle_database_errors
async def get_project_config(
    id: str,
    request: Request,
    db: Session,
):
    user_id = "00000000-0000-0000-0000-000000000001"
    exist_project = db.query(Project).filter(Project.id == id).first()
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
    query = db.query(
        Project.id,
        Project.name,
        Project.config,
    ).filter(Project.id == id)

    project_config = query.first()._asdict()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=make_response(
            message="Lấy danh sách dự án thành công",
            data=jsonable_encoder(project_config),
        ),
    )
