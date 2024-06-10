import os
import requests
import pandas as pd
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from services_python.ml_service.app.schemas import runs as schemas
from services_python.ml_service.app.models import Run, Project
from services_python.utils.name_generator import name_generator
from services_python.utils.api_response import make_response
from services_python.utils.handle_errors_wrapper import handle_database_errors

headers = {"Content-Type": "application/json"}

# Get environment variables
PREFECT_HOST = os.getenv("PREFECT_HOST")
PREFECT_PORT = os.getenv("PREFECT_PORT")
MLFLOW_HOST = os.getenv("MLFLOW_HOST")
MLFLOW_PORT = os.getenv("MLFLOW_PORT")
AWS_ACCESS_KEY_ID = os.getenv("MINIO_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("MINIO_SECRET_ACCESS_KEY")
AWS_ENDPOINT_URL = os.getenv("MINIO_ENDPOINT_URL")

# Set default limit for records
LIMIT_RECORD = int(os.getenv("LIMIT_RECORD", "50"))


@handle_database_errors
async def create_run(
    project_id: str,
    data: schemas.RunCreate,
    request: Request,
    db: Session,
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
    db.refresh(new_run)

    # Create flow run from deployment
    response = requests.post(
        url=f"http://{PREFECT_HOST}:{PREFECT_PORT}/api/deployments/{deployment_id}/create_flow_run",
        headers=headers,
        json={
            "state": {"type": "SCHEDULED"},
            "name": str(new_run.id),
            "parameters": {"run_name": str(new_run.id)},
        },
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
        new_run.flow_run_id = response.json()["id"]
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=make_response(
                message="Khởi chạy dự án thành công",
            ),
        )


@handle_database_errors
async def search_run(
    project_id: str,
    request: Request,
    db: Session,
):
    query_params = dict(request.query_params)
    # Set skip and limit for pagination
    skip = int(query_params.get("skip", 0))
    limit = int(query_params.get("limit", LIMIT_RECORD))
    query = db.query(Run).filter(Run.project_id == project_id)

    # Get total count and records
    total = query.count()
    records = query.offset(skip).limit(limit).all()
    records = [record.to_dict() for record in records]

    if total:
        df = pd.DataFrame(records)
        response = requests.post(
            url=f"http://{PREFECT_HOST}:{PREFECT_PORT}/api/flow_runs/filter/",
            headers=headers,
            json={
                "flow_runs": {
                    "id": {
                        "any_": df["flow_run_id"].tolist(),
                    }
                },
            },
        )
        if 200 <= response.status_code < 300:
            response_df = pd.DataFrame(
                response.json(),
                columns=[
                    "name",
                    "start_time",
                    "end_time",
                    "state_type",
                    "total_run_time",
                ],
            )

            df = df.merge(
                response_df, left_on="id", right_on="name", suffixes=("", "_dev")
            )
            df = df.drop(columns=["name_dev", "run_id", "flow_run_id"])
            records = df.to_dict(orient="records")
        else:
            return JSONResponse(
                status_code=400,
                content=make_response(
                    message="Lấy danh sách thất bại", detail=response.json()
                ),
            )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=make_response(
            message="Lấy danh sách thành công",
            data=records,
            total=total,
            skip=skip,
            limit=limit,
        ),
    )


@handle_database_errors
async def get_run(
    project_id: str,
    run_id: str,
    request: Request,
    db: Session,
):

    exist_run = (
        db.query(Run).filter(Run.id == run_id, Run.project_id == project_id).first()
    )
    if not exist_run:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=make_response(message="Không tìm thấy project_run"),
        )
    exist_run = exist_run.to_dict()

    mlflow_response = requests.get(
        url=f"http://{MLFLOW_HOST}:{MLFLOW_PORT}/api/2.0/mlflow/runs/get",
        headers=headers,
        json={"run_id": exist_run["run_id"]},
    )
    prefect_response = requests.post(
        url=f"http://{PREFECT_HOST}:{PREFECT_PORT}/api/flow_runs/filter/",
        headers=headers,
        json={
            "flow_runs": {
                "id": {
                    "any_": [exist_run["flow_run_id"]],
                }
            },
        },
    )

    if (
        200 <= mlflow_response.status_code < 300
        and 200 <= prefect_response.status_code < 300
    ):
        mlflow_response = mlflow_response.json()["run"]
        prefect_response = prefect_response.json()[0]

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=make_response(
                message="Lấy project_run thành công",
                data={
                    "id": exist_run["id"],
                    "project_id": exist_run["id"],
                    "name": exist_run["name"],
                    "start_time": prefect_response["start_time"],
                    "end_time": prefect_response["end_time"],
                    "state_type": prefect_response["state_type"],
                    "total_run_time": prefect_response["total_run_time"],
                    "artifact_uri": mlflow_response["info"]["artifact_uri"],
                    "metric": mlflow_response["data"]["metrics"],
                },
            ),
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=make_response(
                message="Lấy project_run thất bại",
                detail=prefect_response.json(),
            ),
        )


@handle_database_errors
async def delete_run(
    project_id: str,
    run_id: str,
    request: Request,
    db: Session,
):
    # user_id = "00000000-0000-0000-0000-000000000000"
    exist_run = (
        db.query(Run).filter(Run.id == run_id, Run.project_id == project_id).first()
    )
    if not exist_run:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=make_response(message="Không tìm thấy dự án"),
        )

    db.delete(exist_run)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=make_response(message="Xóa dự án thành công"),
    )


@handle_database_errors
async def update_run(
    project_id: str,
    run_id: str,
    data: schemas.RunUpdate,
    request: Request,
    db: Session,
):
    exist_run = (
        db.query(Run).filter(Run.id == run_id, Run.project_id == project_id).first()
    )
    if not exist_run:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=make_response(message="Không tìm thấy project_run"),
        )
    # Update project data
    for key, value in data.dict().items():
        setattr(exist_run, key, value)

    # Save changes to the database
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Cập nhật project_run thành công"},
    )
