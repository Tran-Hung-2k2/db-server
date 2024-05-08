import os
from sqlalchemy.orm import Session
from fastapi import status, Request, UploadFile
from fastapi.responses import JSONResponse
import json
from services_python.mage_service.app.models import Pipeline, Block, PipelineSchedule
import services_python.mage_service.app.schemas.pipelines as schemas
from services_python.utils.exception import MyException
import services_python.constants.label as label
from services_python.utils.handle_errors_wrapper import handle_database_errors

# from services_python.utils.delta import (
#     save_file_to_s3_as_delta,
#     query_sql_from_delta_table,
# )

import requests  # type: ignore

LIMIT_RECORD = int(os.getenv("LIMIT_RECORD", "50"))

MAGE_HOST = os.getenv("MAGE_HOST", "localhost")
MAGE_PORT = os.getenv("MAGE_PORT", "6789")
MAGE_API_KEY = os.getenv("MAGE_API_KEY", "zkWlN0PkIKSN0C11CfUHUj84OT5XOJ6tDZ6bDRO2")

# HANDLE PIPELINES


@handle_database_errors
def get_all_pipelines(
    db: Session,
    request: Request,
):
    user_id = request.state.id
    query_params = dict(request.query_params)
    # Lấy giá trị skip và limit từ query_params
    skip = int(query_params.get("skip", 0))
    limit = int(query_params.get("limit", LIMIT_RECORD))

    # Giới hạn giá trị limit trong khoảng từ 0 đến 200
    limit = min(max(int(limit), 0), 200)

    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines?tag[]={user_id}&_limit={limit}&_offset={skip}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.get(url, headers=headers)
    data_dict = response.json()
    extracted_data = []

    # Iterate over each pipeline and extract required fields
    for pipeline in data_dict["pipelines"]:
        extracted_pipeline = {
            "created_at": pipeline.get("created_at"),
            "updated_at": pipeline.get("updated_at"),
            "description": pipeline.get("description"),
            "name": db.query(Pipeline).filter((Pipeline.id == pipeline.get("uuid").replace("pipeline_", "").replace('_', '-'))).first().name,
            "settings": pipeline.get("settings"),
            "type": "stream" if pipeline.get("type") == "streaming" else "batch",
            "uuid": pipeline.get("uuid").replace("pipeline_", ""),
            "blocks_number": len(pipeline.get("blocks", [])),
            "schedules_number": len(pipeline.get("schedules", [])),
        }
        extracted_data.append(extracted_pipeline)
    return JSONResponse(
        content={
            "data": extracted_data,
            "skip": skip,
            "limit": limit,
            "total": data_dict["metadata"]["count"],
            "message": "Lấy dữ liệu pipelines thành công",
        },
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def get_one_pipeline(
    uuid: str,
    db: Session,
    request: Request,
):

    exist_pipeline = (
        db.query(Pipeline)
        .filter((Pipeline.id == uuid.replace('_', '-')) & (Pipeline.user_id == request.state.id))
        .first()
    )
    if not exist_pipeline:
        return JSONResponse(
            content={"data": [], "message": "Pipeline không tồn tại"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/pipeline_{uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.get(url, headers=headers)
    data_dict = response.json()
    extracted_data = [
        {
            "created_at": data_dict["pipeline"]["created_at"],
            "updated_at": data_dict["pipeline"]["updated_at"],
            "description": data_dict["pipeline"]["description"],
            "name": exist_pipeline.name,
            "settings": data_dict["pipeline"]["settings"],
            "type": "stream" if data_dict["pipeline"]["type"] == "streaming" else "batch",
            "uuid": data_dict["pipeline"]["uuid"].replace("pipeline_", ""),
            "blocks": [
                {
                    "name": block["name"],
                    "downstream_blocks": block["downstream_blocks"],
                    "type": block["type"],
                    "upstream_blocks": block["upstream_blocks"],
                    "uuid": block["uuid"],
                    "status": block["status"],
                    "conditional_blocks": block["conditional_blocks"],
                    "callback_blocks": block["callback_blocks"],
                    "has_callback": block["has_callback"],
                    "retry_config": block["retry_config"],
                }
                for block in data_dict["pipeline"]["blocks"]
            ],
        }
    ]
    return JSONResponse(
        content={
            "data": extracted_data,
            "skip": 0,
            "limit": 1,
            "total": 1,
            "message": "Lấy dữ liệu một pipeline thành công",
        },
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def create_pipelines(
    data: schemas.PipelineCreate,
    db: Session,
    request: Request,
):
    if not data.name:
        return JSONResponse(
            content={"data": [], "message": "Tên không được để trống"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if not data.type:
        return JSONResponse(
            content={"data": [], "message": "Kiểu không được để trống"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if data.type not in ["batch", "stream"]:
        return JSONResponse(
            content={
                "data": [],
                "message": "Kiểu pipeline không hợp lệ. Kiểu pipeline phải là 'batch' hoặc 'stream'",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    new_record = Pipeline(
        name=data.name, pipeline_type=data.type, user_id=request.state.id
    )
    pipeline_type = new_record.pipeline_type
    description = data.description

    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    extracted_info = {
        "pipeline": {
            "name": ("pipeline_"+str(new_record.id)),
            "type": "streaming" if pipeline_type == "stream" else "python",
            "tags": [str(new_record.user_id)],
            "description": description,
        }
    }
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.post(url, json=extracted_info, headers=headers)
    data_dict = response.json()
    if "error" not in data_dict:
        pipeline = data_dict["pipeline"]
        extracted_pipeline = {
            "created_at": pipeline.get("created_at"),
            "updated_at": pipeline.get("updated_at"),
            "description": pipeline.get("description"),
            "name": new_record.name,
            "settings": pipeline.get("settings"),
            "type": "stream" if pipeline.get("type") == "streaming" else "batch",
            "uuid": pipeline.get("uuid").replace("pipeline_", ""),
            # "variables_dir": pipeline.get("variables_dir"),
            "blocks_number": len(pipeline.get("blocks", [])),
            "schedules_number": len(pipeline.get("schedules", [])),
        }
        extracted_data = [extracted_pipeline]
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": "",
                "message": "Tạo pipeline thành công",
            },
            status_code=status.HTTP_200_OK,
        )
    else:
        extracted_data = []
        detail = data_dict["error"]["exception"]
        db.delete(new_record)
        db.commit()
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": detail,
                "message": "Tạo pipelines thất bại",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@handle_database_errors
def delete_one_pipeline(
    uuid: str,
    db: Session,
    request: Request,
):
    exist_pipeline = (
        db.query(Pipeline)
        .filter((Pipeline.id == uuid.replace('_', '-')) & (Pipeline.user_id == request.state.id))
        .first()
    )
    if not exist_pipeline:
        return JSONResponse(
            content={"data": [], "message": "Pipeline không tồn tại"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/pipeline_{uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.delete(url, headers=headers)
    data_dict = response.json()

    if "error" not in data_dict:
        pipeline = data_dict["pipeline"]
        extracted_pipeline = {
            "created_at": pipeline.get("created_at"),
            "updated_at": pipeline.get("updated_at"),
            "description": pipeline.get("description"),
            "name": exist_pipeline.name,
            "settings": pipeline.get("settings"),
            "tags": pipeline.get("tags"),
            "type": "stream" if pipeline.get("type") == "streaming" else "batch",
            "uuid": pipeline.get("uuid").replace("pipeline_", ""),
            "variables_dir": pipeline.get("variables_dir"),
            "blocks_number": len(pipeline.get("blocks", [])),
            "schedules_number": len(pipeline.get("schedules", [])),
        }
        extracted_data = [extracted_pipeline]
        db.delete(exist_pipeline)
        db.commit()
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": [],
                "message": "Xóa pipeline thành công.",
            },
            status_code=status.HTTP_200_OK,
        )
    else:
        extracted_data = []
        detail = data_dict["error"]["exception"]
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": detail,
                "message": "Xóa pipeline thất bại.",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )


# HANDLE BLOCKS
@handle_database_errors
def get_one_block(
    uuid: str,
    block_uuid: str,
    db: Session,
    request: Request,
):
    exist_block = (
        db.query(Block)
        .join(Pipeline, Pipeline.id == Block.pipeline_id)
        .filter(Block.id == block_uuid)
        .with_entities(Pipeline.id)
        .first()
    )
    if not exist_block:
        return JSONResponse(
            content={"data": [], "message": "Block không tồn tại"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if exist_block.user_id != request.state.id:
        return JSONResponse(
            content={"data": [], "message": "Bạn không có quyền truy cập block"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    print(exist_block)
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/blocks/{block_uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.get(url, headers=headers)
    data_dict = response.json()
    extracted_data = [
        {
            "name": data_dict["block"]["name"],
            "downstream_blocks": data_dict["block"]["downstream_blocks"],
            "type": data_dict["block"]["type"],
            "upstream_blocks": data_dict["block"]["upstream_blocks"],
            "uuid": data_dict["block"]["uuid"],
            "status": data_dict["block"]["status"],
            # "conditional_blocks": [],
            # "callback_blocks": [],
            "has_callback": data_dict["block"]["has_callback"],
            "retry_config": data_dict["block"]["retry_config"],
            "content": data_dict["block"]["content"],
        }
    ]
    return JSONResponse(
        content={
            "data": extracted_data,
            "skip": 0,
            "limit": 1,
            "total": 1,
            "message": "Lấy dữ liệu một block thành công",
        },
        status_code=status.HTTP_200_OK,
    )


def get_block_content(block_type, source_type, source_config):
    if block_type == "data_loader":
        if source_type == "postgres":
            from services_python.mage_service.template.datasource.postgres import (
                get_string,
                check_config_keys,
            )

            if check_config_keys(source_config):
                return get_string(source_config)
        elif source_type == "mysql":
            pass
        elif source_type == "mongodb":
            pass
        elif source_type == "amazon_s3":
            pass
        elif source_type == "test":
            return "Hello worldd"
        else:
            pass
    elif block_type == "data_exporter":
        pass


@handle_database_errors
def create_block(
    uuid: str,
    data: schemas.BlockCreate,
    db: Session,
    request: Request,
):
    new_record = Block(
        name=data.name,
        pipeline_id=uuid,
        source_type=data.source_type,
        source_config=data.source_config,
        block_type=data.block_type,
    )
    db.commit()
    db.refresh(new_record)
    name = str(new_record.id)
    block_type = new_record.block_type
    source_type = new_record.source_type
    source_config = new_record.source_config
    content = get_block_content(block_type, source_type, source_config)
    language = "python"
    extracted_info = {
        "block": {
            "name": name,
            "type": block_type,
            "content": content,
            "language": language,
            # "color": color,
            # "config": config,
            # "configuration": configuration,
            # "extension_uuid": extension_uuid,
            # "pipelines": pipelines,
            # "priority": priority,
            # "upstream_blocks": upstream_blocks
        }
    }

    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/blocks"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.post(url, json=extracted_info, headers=headers)
    data_dict = response.json()
    if "error" not in data_dict:
        extracted_data = [
            {
                "name": data_dict["block"]["name"],
                "downstream_blocks": data_dict["block"]["downstream_blocks"],
                "type": data_dict["block"]["type"],
                "upstream_blocks": data_dict["block"]["upstream_blocks"],
                "uuid": data_dict["block"]["uuid"],
                "status": data_dict["block"]["status"],
                # "conditional_blocks": [],
                # "callback_blocks": [],
                "has_callback": data_dict["block"]["has_callback"],
                "retry_config": data_dict["block"]["retry_config"],
                "content": data_dict["block"]["content"],
            }
        ]
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": "",
                "message": "Tạo block thành công",
            },
            status_code=status.HTTP_200_OK,
        )
    else:
        extracted_data = []
        detail = data_dict["error"]["exception"]
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": detail,
                "message": "Tạo block thất bại",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@handle_database_errors
def update_block(
    uuid: str,
    block_uuid: str,
    data: schemas.BlockUpdate,
    db: Session,
    request: Request,
):
    name = data.name
    block_type = data.block_type
    source_config = data.source_config
    source_type = data.source_type
    content = get_block_content(block_type, source_type, source_config)
    downstream_blocks = data.downstream_blocks
    upstream_blocks = data.upstream_blocks
    conditional_blocks = data.conditional_blocks
    callback_blocks = data.callback_blocks
    has_callback = data.has_callback
    retry_config = data.retry_config
    updated_block = {
        "block": {
            "name": name,
            "type": block_type,
            "content": content,
            "downstream_blocks": downstream_blocks,
            "upstream_blocks": upstream_blocks,
            "conditional_blocks": conditional_blocks,
            "callback_blocks": callback_blocks,
            "has_callback": has_callback,
            "retry_config": retry_config,
            # "bookmark_values": bookmark_values,
            # "callback_blocks": callback_blocks,
            # "color": color,
            # "configuration": configuration,
            # "destination_table": destination_table,
            # "executor_config": executor_config,
            # "executor_type": executor_type,
            # "extension_uuid": extension_uuid,
            # "language": language,
            # "pipelines": pipelines,
            # "retry_config": retry_config,
            # "tap_stream_id": tap_stream_id,
        }
    }

    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/blocks/{block_uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.put(url, json=updated_block, headers=headers)
    data_dict = response.json()
    if "error" not in data_dict:
        extracted_data = [
            {
                "name": data_dict["block"]["name"],
                "downstream_blocks": data_dict["block"]["downstream_blocks"],
                "type": data_dict["block"]["type"],
                "upstream_blocks": data_dict["block"]["upstream_blocks"],
                "uuid": data_dict["block"]["uuid"],
                "status": data_dict["block"]["status"],
                # "conditional_blocks": [],
                # "callback_blocks": [],
                "has_callback": data_dict["block"]["has_callback"],
                "retry_config": data_dict["block"]["retry_config"],
                "content": data_dict["block"]["content"],
            }
        ]
        message = "Sửa block thành công"
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": detail,
                "message": message,
            },
            status_code=status.HTTP_200_OK,
        )
    else:
        extracted_data = {}
        detail = data_dict["error"]["exception"]
        message = "Sửa block thất bại"
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": detail,
                "message": message,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@handle_database_errors
def delete_one_block(
    uuid: str,
    block_uuid: str,
    db: Session,
    request: Request,
):
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/blocks/{block_uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.delete(url, headers=headers)
    data_dict = response.json()
    if "error" not in data_dict:
        extracted_data = {
            "blocks": [
                {
                    "name": data_dict["block"]["name"],
                    "downstream_blocks": data_dict["block"]["downstream_blocks"],
                    "type": data_dict["block"]["type"],
                    "upstream_blocks": data_dict["block"]["upstream_blocks"],
                    "uuid": data_dict["block"]["uuid"],
                    "status": data_dict["block"]["status"],
                    # "conditional_blocks": [],
                    # "callback_blocks": [],
                    "has_callback": data_dict["block"]["has_callback"],
                    "retry_config": data_dict["block"]["retry_config"],
                }
            ],
            "metadata": data_dict["metadata"],
        }
        message = "Xóa block thành công"
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": detail,
                "message": message,
            },
            status_code=status.HTTP_200_OK,
        )
    else:
        extracted_data = {}
        detail = data_dict["error"]["exception"]
        message = "Xóa block thất bại"
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": detail,
                "message": message,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )


# HANDLE TRIGGERS


@handle_database_errors
def get_all_pipeline_schedules(
    uuid: str,
    db: Session,
    request: Request,
):
    query_params = dict(request.query_params)
    # Lấy giá trị skip và limit từ query_params
    skip = int(query_params.get("skip", 0))
    limit = int(query_params.get("limit", LIMIT_RECORD))

    # Giới hạn giá trị limit trong khoảng từ 0 đến 200
    limit = min(max(int(limit), 0), 200)

    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/pipeline_schedules?_limit={limit}&_offset={skip}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.get(url, headers=headers)
    data_dict = response.json()
    extracted_data = {
        "pipeline_schedules": [
            {
                "created_at": schedule["created_at"],
                "updated_at": schedule["updated_at"],
                "description": schedule["description"],
                "name": schedule["name"],
                "settings": schedule["settings"],
                "tags": schedule["tags"],
                "id": schedule["id"],
                "last_enabled_at": schedule["last_enabled_at"],
                "pipeline_uuid": schedule["pipeline_uuid"],
                "schedule_interval": schedule["schedule_interval"],
                "schedule_type": schedule["schedule_type"],
                "start_time": schedule["start_time"],
                "status": schedule["status"],
                "token": schedule["token"],
                # "variables": schedule["variables"],
                "last_pipeline_run_status": schedule["last_pipeline_run_status"],
                "next_pipeline_run_date": schedule["next_pipeline_run_date"],
                "pipeline_in_progress_runs_count": schedule[
                    "pipeline_in_progress_runs_count"
                ],
                "pipeline_runs_count": schedule["pipeline_runs_count"],
            }
            for schedule in data_dict["pipeline_schedules"]
        ],
        "metadata": {"count": data_dict["metadata"]["count"]},
    }
    return JSONResponse(
        content={
            "data": extracted_data,
            "skip": skip,
            "limit": limit,
            "total": data_dict["metadata"]["count"],
            "message": "Lấy dữ liệu schedule thành công",
        },
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def create_pipeline_schedules(
    uuid: str,
    data: schemas.PipelineScheduleCreate,
    db: Session,
    request: Request,
):
    name = data.name
    id = data.id
    description = data.description
    schedule_interval = data.schedule_interval
    schedule_type = data.schedule_type
    settings = data.settings
    start_time = data.start_time
    pipeline_schedule = {
        "pipeline_schedule": {
            "name": name,
            "id": id,
            "description": description,
            "schedule_interval": schedule_interval,
            "schedule_type": schedule_type,
            "settings": settings,
            "start_time": start_time,
        }
    }

    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/pipeline_schedules"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.post(url, json=pipeline_schedule, headers=headers)
    data_dict = response.json()
    print(data_dict)
    if "error" not in data_dict:
        extracted_data = {
            "pipeline_schedule": [
                {
                    "created_at": data_dict["pipeline_schedule"]["created_at"],
                    "updated_at": data_dict["pipeline_schedule"]["updated_at"],
                    "description": data_dict["pipeline_schedule"]["description"],
                    "name": data_dict["pipeline_schedule"]["name"],
                    "settings": data_dict["pipeline_schedule"]["settings"],
                    # "tags": data_dict["pipeline_schedule"]["tags"],
                    "id": data_dict["pipeline_schedule"]["id"],
                    "last_enabled_at": data_dict["pipeline_schedule"][
                        "last_enabled_at"
                    ],
                    "pipeline_uuid": data_dict["pipeline_schedule"]["pipeline_uuid"],
                    "schedule_interval": data_dict["pipeline_schedule"][
                        "schedule_interval"
                    ],
                    "schedule_type": data_dict["pipeline_schedule"]["schedule_type"],
                    "start_time": data_dict["pipeline_schedule"]["start_time"],
                    "status": data_dict["pipeline_schedule"]["status"],
                    "token": data_dict["pipeline_schedule"]["token"],
                    # "variables": data_dict["pipeline_schedule"]["variables"],
                }
            ],
            "metadata": data_dict["metadata"],
        }
        message = "Tạo schedule thành công"
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": detail,
                "message": message,
            },
            status_code=status.HTTP_200_OK,
        )
    else:
        extracted_data = {}
        detail = data_dict["error"]["exception"]
        message = "Tạo schedule thất bại"
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": detail,
                "message": message,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@handle_database_errors
def update_pipeline_schedules(
    pipeline_schedules_uuid: str,
    data: schemas.PipelineScheduleUpdate,
    uuid: str,
    db: Session,
    request: Request,
):
    name = data.name
    description = data.description
    schedule_interval = data.schedule_interval
    schedule_type = data.schedule_type
    settings = data.settings
    start_time = data.start_time
    my_status = data.status
    tags = data.tags
    pipeline_schedule = {
        "pipeline_schedule": {
            "name": name,
            "description": description,
            "schedule_interval": schedule_interval,
            "schedule_type": schedule_type,
            "settings": settings,
            "start_time": start_time,
            "status": my_status,
            # "tags": [tags],
        }
    }

    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/pipeline_schedules/{pipeline_schedules_uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.post(url, json=pipeline_schedule, headers=headers)
    data_dict = response.json()
    if "error" not in data_dict:
        extracted_data = {
            "pipeline_schedule": [
                {
                    "created_at": data_dict["pipeline_schedule"]["created_at"],
                    "updated_at": data_dict["pipeline_schedule"]["updated_at"],
                    "description": data_dict["pipeline_schedule"]["description"],
                    "name": data_dict["pipeline_schedule"]["name"],
                    "settings": data_dict["pipeline_schedule"]["settings"],
                    # "tags": data_dict["pipeline_schedule"]["tags"],
                    "id": data_dict["pipeline_schedule"]["id"],
                    "last_enabled_at": data_dict["pipeline_schedule"][
                        "last_enabled_at"
                    ],
                    "pipeline_uuid": data_dict["pipeline_schedule"]["pipeline_uuid"],
                    "schedule_interval": data_dict["pipeline_schedule"][
                        "schedule_interval"
                    ],
                    "schedule_type": data_dict["pipeline_schedule"]["schedule_type"],
                    "start_time": data_dict["pipeline_schedule"]["start_time"],
                    "status": data_dict["pipeline_schedule"]["status"],
                    "token": data_dict["pipeline_schedule"]["token"],
                    # "variables": data_dict["pipeline_schedule"]["variables"],
                    "last_pipeline_run_status": data_dict["pipeline_schedule"][
                        "last_pipeline_run_status"
                    ],
                    "next_pipeline_run_date": data_dict["pipeline_schedule"][
                        "next_pipeline_run_date"
                    ],
                    "pipeline_in_progress_runs_count": data_dict["pipeline_schedule"][
                        "pipeline_in_progress_runs_count"
                    ],
                    "pipeline_runs_count": data_dict["pipeline_schedule"][
                        "pipeline_runs_count"
                    ],
                }
            ],
            "metadata": data_dict["metadata"],
        }
        message = "Sửa schedule thành công"
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": detail,
                "message": message,
            },
            status_code=status.HTTP_200_OK,
        )
    else:
        extracted_data = {}
        detail = data_dict["error"]["exception"]
        message = "Sửa schedule thất bại"

        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": detail,
                "message": message,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@handle_database_errors
def delete_one_pipeline_schedules(
    uuid: str,
    pipeline_schedules_uuid: str,
    db: Session,
    request: Request,
):
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/pipeline_schedules/{pipeline_schedules_uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.delete(url, headers=headers)
    data_dict = response.json()
    print(data_dict)
    if "error" not in data_dict:
        extracted_data = {
            "pipeline_schedule": [
                {
                    "created_at": data_dict["pipeline_schedule"]["created_at"],
                    "updated_at": data_dict["pipeline_schedule"]["updated_at"],
                    "description": data_dict["pipeline_schedule"]["description"],
                    "name": data_dict["pipeline_schedule"]["name"],
                    "settings": data_dict["pipeline_schedule"]["settings"],
                    "id": data_dict["pipeline_schedule"]["id"],
                    "last_enabled_at": data_dict["pipeline_schedule"][
                        "last_enabled_at"
                    ],
                    "pipeline_uuid": data_dict["pipeline_schedule"]["pipeline_uuid"],
                    "schedule_interval": data_dict["pipeline_schedule"][
                        "schedule_interval"
                    ],
                    "schedule_type": data_dict["pipeline_schedule"]["schedule_type"],
                    "start_time": data_dict["pipeline_schedule"]["start_time"],
                    "status": data_dict["pipeline_schedule"]["status"],
                    "token": data_dict["pipeline_schedule"]["token"],
                    # "variables": data_dict["pipeline_schedule"]["variables"],
                }
            ],
            "metadata": data_dict["metadata"],
        }
        message = "Xóa schedule thành công"
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": detail,
                "message": message,
            },
            status_code=status.HTTP_200_OK,
        )
    else:
        extracted_data = {}
        detail = data_dict["error"]["exception"]
        message = "Xóa schedule thất bại"
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": detail,
                "message": message,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
