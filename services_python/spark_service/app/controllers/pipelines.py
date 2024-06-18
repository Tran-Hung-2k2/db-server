import os
from sqlalchemy.orm import Session
from fastapi import status, Request, UploadFile
from fastapi.responses import JSONResponse
import json
from services_python.spark_service.app.models import Pipeline, Block, PipelineSchedule
import services_python.spark_service.app.schemas.pipelines as schemas
from services_python.utils.exception import MyException
import services_python.constants.label as label
from services_python.utils.handle_errors_wrapper import handle_database_errors
from unidecode import unidecode


import requests  # type: ignore

LIMIT_RECORD = int(os.getenv("LIMIT_RECORD", "50"))

MAGE_HOST = os.getenv("MAGE_HOST", "localhost")
MAGE_PORT = os.getenv("MAGE_PORT", "6789")
MAGE_API_KEY = os.getenv("MAGE_API_KEY", "zkWlN0PkIKSN0C11CfUHUj84OT5XOJ6tDZ6bDRO2")

AIRFLOW_HOST = os.getenv("AIRFLOW_HOST", "localhost")
AIRFLOW_PORT = os.getenv("AIRFLOW_PORT", "7788")
AIRFLOW_API_KEY = os.getenv("AIRFLOW_API_KEY", "Basic YWRtaW46MQ==")

# HANDLE PIPELINES


@handle_database_errors
async def get_all_pipelines(
    db: Session,
    request: Request,
):
    user_id = request.state.id
    query_params = dict(request.query_params)
    skip = int(query_params.get("skip", 0))
    limit = int(query_params.get("limit", LIMIT_RECORD))
    limit = min(max(int(limit), 0), 200)
    sort_by = query_params.get("sort_by", "name").lower()
    if sort_by not in ["dag_display_name"]:
        sort_by = "dag_display_name"
    sort_dim = query_params.get("sort_dim", "desc").lower()
    if sort_dim not in ["desc"]:
        sort_dim = "-"
    else:
        sort_dim = ""
    params = {
        'tags': user_id,
        'limit': limit,
        'offset': skip,
        'order_by': f"{sort_dim}{sort_by}",
        'fields':"dag_id,dag_display_name,description,is_active,schedule_interval"
    }

    url = f"http://{AIRFLOW_HOST}:{AIRFLOW_PORT}/api/v1/dags"
    headers = {"Authorization": AIRFLOW_API_KEY}
    response = requests.get(url, headers=headers, params=params)
    data_dict = response.json()
    extracted_data = []
    for pipeline in data_dict["dags"]:
        exist_pipeline = (
            db.query(Pipeline)
            .filter(
                (Pipeline.id == pipeline.get("dag_id").replace("_", "-"))
                & (Pipeline.user_id == request.state.id)
            )
            .first()
        )
        block_number = (
            db.query(Block).filter(Block.pipeline_id == exist_pipeline.id).count()
        )
        schedule_number = (
            db.query(PipelineSchedule).filter(PipelineSchedule.pipeline_id == exist_pipeline.id).count()
        )
        extracted_pipeline = {
            "created_at": exist_pipeline.created_at,
            "updated_at": exist_pipeline.updated_at,
            "description": pipeline.get("description"),
            "name": exist_pipeline.name,
            "settings": None,
            "type": exist_pipeline.pipeline_type,
            "uuid": pipeline.get("dag_id"),
            "blocks_number": block_number,
            "schedules_number": schedule_number,
            "status": "active" if pipeline.get("is_active") else "inactive",
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
async def get_one_pipeline(
    uuid: str,
    db: Session,
    request: Request,
):

    exist_pipeline = (
        db.query(Pipeline)
        .filter(
            (Pipeline.id == uuid.replace("_", "-"))
            & (Pipeline.user_id == request.state.id)
        )
        .first()
    )
    if not exist_pipeline:
        return JSONResponse(
            content={"data": [], "message": "Pipeline không tồn tại"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


    url = f"http://{AIRFLOW_HOST}:{AIRFLOW_PORT}/api/v1/dags/{uuid}/tasks"
    headers = {"Authorization": AIRFLOW_API_KEY}
    response = requests.get(url, headers=headers)
    data_dict = response.json()

    extracted_data = [
        {
            "created_at": exist_pipeline.created_at,
            "updated_at": exist_pipeline.updated_at,
            # "description": data_dict["pipeline"]["description"],
            "name": exist_pipeline.name,
            "settings": None,
            "type": exist_pipeline.pipeline_type,
            "uuid": uuid,
            "blocks": [
                {
                    "name": block["task_display_name"],
                    "downstream_blocks": block["downstream_task_ids"],
                    "type": db.query(Block)
                    .filter(Block.id == block["task_id"].replace("_", "-"))
                    .first()
                    .block_type,
                    # "upstream_blocks": block["upstream_blocks"][-36:],
                    # "uuid": block["task_id"],
                    # "status": block["status"],
                    # "conditional_blocks": block["conditional_blocks"],
                    # "callback_blocks": block["callback_blocks"],
                    # "has_callback": block["has_callback"],
                    "retry_config": block["retry_delay"],
                }
                for block in data_dict["tasks"]
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


from services_python.spark_service.template.generate_dag import generate_dag


@handle_database_errors
async def create_pipelines(
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
    description = data.description

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    extracted_info = {
        "dag_name": new_record.name,
        "dag_id": str(new_record.id).replace("-", "_"),
        "user_id": [str(new_record.user_id).replace("-", "_")],
        "description": description,
    }
    if generate_dag(extracted_info):
        extracted_pipeline = {
            "created_at": new_record.created_at,
            "updated_at": new_record.updated_at,
            "description": description,
            "name": new_record.name,
            "settings": None,
            "type": new_record.pipeline_type,
            "uuid": new_record.id.replace("-", "_"),
            # "variables_dir": pipeline.get("variables_dir"),
            "blocks_number": 0,
            "schedules_number": 0,
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
        detail = ["Error when creating DAG"]
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
async def update_pipeline(
    data: schemas.PipelineUpdate,
    uuid: str,
    db: Session,
    request: Request,
):
    exist_pipeline = (
        db.query(Pipeline)
        .filter(
            (Pipeline.id == uuid.replace("_", "-"))
            & (Pipeline.user_id == request.state.id)
        )
        .first()
    )
    if not exist_pipeline:
        return JSONResponse(
            content={"data": [], "message": "Pipeline không tồn tại"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/pipeline_{unidecode(exist_pipeline.name).replace(' ', '_').lower()}_{uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    extracted_info = {
        "pipeline": {
            "name": (
                "pipeline_"
                + unidecode(data.name.replace(" ", "_"))
                + "_"
                + str(exist_pipeline.id)
            ),
            "type": "streaming" if exist_pipeline == "stream" else "python",
            "tags": [str(exist_pipeline.user_id)],
            "description": data.description,
        }
    }

    response = requests.put(url, json=extracted_info, headers=headers)
    data_dict = response.json()
    if "error" not in data_dict:
        updated_data_dict = data.dict()
        for key, value in updated_data_dict.items():
            setattr(exist_pipeline, key, value)
        db.commit()
        db.refresh(exist_pipeline)
        pipeline = data_dict["pipeline"]
        extracted_pipeline = {
            "created_at": pipeline.get("created_at"),
            "updated_at": pipeline.get("updated_at"),
            "description": pipeline.get("description"),
            "name": exist_pipeline.name,
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
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": detail,
                "message": "Tạo pipelines thất bại",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@handle_database_errors
async def delete_one_pipeline(
    uuid: str,
    db: Session,
    request: Request,
):
    exist_pipeline = (
        db.query(Pipeline)
        .filter(
            (Pipeline.id == uuid.replace("_", "-"))
            & (Pipeline.user_id == request.state.id)
        )
        .first()
    )
    if not exist_pipeline:
        return JSONResponse(
            content={"data": [], "message": "Pipeline không tồn tại"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/pipeline_{unidecode(exist_pipeline.name).replace(' ', '_').lower()}_{uuid}"
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
async def get_one_block(
    uuid: str,
    block_uuid: str,
    db: Session,
    request: Request,
):
    exist_pipeline = (
        db.query(Pipeline)
        .filter(
            (Pipeline.id == uuid.replace("_", "-"))
            & (Pipeline.user_id == request.state.id)
        )
        .first()
    )
    if not exist_pipeline:
        return JSONResponse(
            content={"data": [], "message": "Pipeline không tồn tại"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    exist_block = (
        db.query(Block).filter(Block.id == block_uuid.replace("_", "-")).first()
    )
    if not exist_block:
        return JSONResponse(
            content={"data": [], "message": "Block không tồn tại"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if exist_block.pipeline_id != exist_pipeline.id:
        return JSONResponse(
            content={"data": [], "message": "Bạn không có quyền truy cập block này"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/pipeline_{unidecode(exist_pipeline.name).replace(' ', '_').lower()}_{uuid}/blocks/block_{unidecode(exist_block.name).replace(' ', '_').lower()}_{block_uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.get(url, headers=headers)
    data_dict = response.json()
    extracted_data = [
        {
            "name": exist_block.name,
            "downstream_blocks": [
                downstream_block[-36:]
                for downstream_block in data_dict["block"]["downstream_blocks"]
            ],
            "type": data_dict["block"]["type"],
            "upstream_blocks": [
                upstream_block[-36:]
                for upstream_block in data_dict["block"]["upstream_blocks"]
            ],
            "uuid": data_dict["block"]["uuid"][-36:],
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


@handle_database_errors
async def create_block(
    uuid: str,
    data: schemas.BlockCreate,
    db: Session,
    request: Request,
):
    if not data.name:
        return JSONResponse(
            content={"data": [], "message": "Tên block không được để trống"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if not data.block_type:
        return JSONResponse(
            content={"data": [], "message": "Kiểu block không được để trống"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if not data.source_type:
        return JSONResponse(
            content={"data": [], "message": "Kiểu source không được để trống"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if not data.source_config:
        return JSONResponse(
            content={"data": [], "message": "Cấu hình source không được để trống"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if data.block_type not in ["data_loader", "transformer", "data_exporter"]:
        return JSONResponse(
            content={
                "data": [],
                "message": "Kiểu block không hợp lệ. Kiểu block phải là 'data_loader', 'transformer', hoặc 'data_exporter'",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    exist_pipeline = (
        db.query(Pipeline)
        .filter(
            (Pipeline.id == uuid.replace("_", "-"))
            & (Pipeline.user_id == request.state.id)
        )
        .first()
    )
    if not exist_pipeline:
        return JSONResponse(
            content={"data": [], "message": "Pipeline không tồn tại"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    new_record = Block(
        name=data.name,
        pipeline_id=exist_pipeline.id,
        source_type=data.source_type,
        source_config=json.dumps(data.source_config),
        block_type=data.block_type,
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    content = get_block_content(
        block_type=new_record.block_type,
        source_type=new_record.source_type,
        source_config=json.loads(new_record.source_config),
    )
    language = "python"
    extracted_info = {
        "block": {
            "name": "block_"
            + unidecode(new_record.name.replace(" ", "_"))
            + "_"
            + str(new_record.id),
            "type": new_record.block_type,
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
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/pipeline_{unidecode(exist_pipeline.name).replace(' ', '_').lower()}_{uuid}/blocks"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.post(url, json=extracted_info, headers=headers)
    data_dict = response.json()
    if "error" not in data_dict:
        extracted_data = [
            {
                "name": new_record.name,
                "downstream_blocks": [
                    downstream_block[-36:]
                    for downstream_block in data_dict["block"]["downstream_blocks"]
                ],
                "type": data_dict["block"]["type"],
                "upstream_blocks": [
                    upstream_block[-36:]
                    for upstream_block in data_dict["block"]["upstream_blocks"]
                ],
                "uuid": data_dict["block"]["uuid"][-36:],
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
        db.delete(new_record)
        db.commit()
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": detail,
                "message": "Tạo block thất bại",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@handle_database_errors
async def update_block(
    uuid: str,
    block_uuid: str,
    data: schemas.BlockUpdate,
    db: Session,
    request: Request,
):
    exist_pipeline = (
        db.query(Pipeline)
        .filter(
            (Pipeline.id == uuid.replace("_", "-"))
            & (Pipeline.user_id == request.state.id)
        )
        .first()
    )
    if not exist_pipeline:
        return JSONResponse(
            content={"data": [], "message": "Pipeline không tồn tại"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    exist_block = (
        db.query(Block).filter(Block.id == block_uuid.replace("_", "-")).first()
    )
    if not exist_block:
        return JSONResponse(
            content={"data": [], "message": "Block không tồn tại"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if exist_block.pipeline_id != exist_pipeline.id:
        return JSONResponse(
            content={"data": [], "message": "Bạn không có quyền truy cập block này"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    content = get_block_content(
        block_type=data.block_type,
        source_type=data.source_type,
        source_config=data.source_config,
    )
    downstream_blocks = data.downstream_blocks
    upstream_blocks = data.upstream_blocks
    conditional_blocks = data.conditional_blocks
    callback_blocks = data.callback_blocks
    updated_block = {
        "block": {
            "content": content if content else "",
            "downstream_blocks": [
                f'block_{unidecode(db.query(Block).filter(Block.id == downstream_block_id.replace("_", "-")).first().name).lower().replace(" ", "_")}_{downstream_block_id}'
                for downstream_block_id in downstream_blocks
            ],
            "upstream_blocks": [
                f'block_{unidecode(db.query(Block).filter(Block.id == upstream_block_id.replace("_", "-")).first().name).lower().replace(" ", "_")}_{upstream_block_id}'
                for upstream_block_id in upstream_blocks
            ],
            "conditional_blocks": [
                f'block_{unidecode(db.query(Block).filter(Block.id == conditional_block_id.replace("_", "-")).first().name).lower().replace(" ", "_")}'
                for conditional_block_id in conditional_blocks
            ],
            "callback_blocks": [
                f'block_{unidecode(db.query(Block).filter(Block.id == callback_block_id.replace("_", "-")).first().name).lower().replace(" ", "_")}'
                for callback_block_id in callback_blocks
            ],
            "has_callback": True if data.has_callback else False,
            "retry_config": data.retry_config if data.has_callback else [],
        }
    }
    if data.block_type:
        updated_block["block"]["type"] = data.block_type
    if data.name:
        updated_block["block"]["name"] = (
            "block_"
            + unidecode(data.name.replace(" ", "_"))
            + "_"
            + str(exist_block.id)
        )
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/pipeline_{unidecode(exist_pipeline.name).replace(' ', '_').lower()}_{uuid}/blocks/block_{unidecode(exist_block.name).replace(' ', '_').lower()}_{block_uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.put(url, json=updated_block, headers=headers)
    data_dict = response.json()
    if "error" not in data_dict:
        if data.name:
            setattr(exist_block, "name", data.name)
        if data.source_config:
            setattr(exist_block, "source_config", data.source_config)
        if data.source_type:
            setattr(exist_block, "source_type", data.source_type)
        if data.block_type:
            setattr(exist_block, "block_type", data.block_type)
        db.commit()
        db.refresh(exist_block)
        extracted_data = [
            {
                "name": exist_block.name,
                "downstream_blocks": [
                    downstream_block[-36:]
                    for downstream_block in data_dict["block"]["downstream_blocks"]
                ],
                "type": data_dict["block"]["type"],
                "upstream_blocks": [
                    upstream_block[-36:]
                    for upstream_block in data_dict["block"]["upstream_blocks"]
                ],
                "uuid": data_dict["block"]["uuid"][-36:],
                "status": data_dict["block"]["status"],
                # "conditional_blocks": [],
                # "callback_blocks": [],
                "has_callback": data_dict["block"]["has_callback"],
                "retry_config": data_dict["block"]["retry_config"],
                "content": data_dict["block"]["content"],
            }
        ]
        message = "Sửa block thành công"

        # TODO update database

        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": [],
                "message": message,
            },
            status_code=status.HTTP_200_OK,
        )
    else:
        extracted_data = []
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
async def delete_one_block(
    uuid: str,
    block_uuid: str,
    db: Session,
    request: Request,
):
    exist_pipeline = (
        db.query(Pipeline)
        .filter(
            (Pipeline.id == uuid.replace("_", "-"))
            & (Pipeline.user_id == request.state.id)
        )
        .first()
    )
    if not exist_pipeline:
        return JSONResponse(
            content={"data": [], "message": "Pipeline không tồn tại"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    exist_block = (
        db.query(Block).filter(Block.id == block_uuid.replace("_", "-")).first()
    )
    if not exist_block:
        return JSONResponse(
            content={"data": [], "message": "Block không tồn tại"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if exist_block.pipeline_id != exist_pipeline.id:
        return JSONResponse(
            content={"data": [], "message": "Bạn không có quyền truy cập block này"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/pipeline_{unidecode(exist_pipeline.name).replace(' ', '_').lower()}_{uuid}/blocks/block_{unidecode(exist_block.name).replace(' ', '_').lower()}_{block_uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.delete(url, headers=headers)
    data_dict = response.json()
    if "error" not in data_dict:
        extracted_data = [
            {
                "name": exist_block.name,
                "downstream_blocks": [
                    downstream_block[-36:]
                    for downstream_block in data_dict["block"]["downstream_blocks"]
                ],
                "type": data_dict["block"]["type"],
                "upstream_blocks": [
                    upstream_block[-36:]
                    for upstream_block in data_dict["block"]["upstream_blocks"]
                ],
                "uuid": data_dict["block"]["uuid"][-36:],
                "status": data_dict["block"]["status"],
                # "conditional_blocks": [],
                # "callback_blocks": [],
                "has_callback": data_dict["block"]["has_callback"],
                "retry_config": data_dict["block"]["retry_config"],
            }
        ]
        db.delete(exist_block)
        db.commit()
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
        extracted_data = []
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
async def get_all_pipeline_schedules(
    uuid: str,
    db: Session,
    request: Request,
):

    query_params = dict(request.query_params)
    skip = int(query_params.get("skip", 0))
    limit = int(query_params.get("limit", LIMIT_RECORD))
    limit = min(max(int(limit), 0), 200)

    schedule_pipeline_type = query_params.get("type", "").lower()
    if schedule_pipeline_type in ["api"]:
        schedule_pipeline_type = "&schedule_type[]=api"
    elif schedule_pipeline_type in ["time"]:
        schedule_pipeline_type = "&schedule_type[]=time"
    else:
        schedule_pipeline_type = ""

    schedule_pipeline_interval = query_params.get("interval", "").lower()
    if schedule_pipeline_interval in ["once"]:
        schedule_pipeline_interval = "&schedule_interval[]=@once"
    elif schedule_pipeline_interval in ["hourly"]:
        schedule_pipeline_interval = "&schedule_interval[]=@hourly"
    else:
        schedule_pipeline_interval = ""
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/pipeline_schedules?_limit={limit}&_offset={skip}{schedule_pipeline_type}{schedule_pipeline_interval}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.get(url, headers=headers)
    data_dict = response.json()
    extracted_data = [
        {
            "created_at": schedule["created_at"],
            "updated_at": schedule["updated_at"],
            "description": schedule["description"],
            "name": db.query(PipelineSchedule)
            .filter((PipelineSchedule.id == schedule.get("id").replace("_", "-")))
            .first()
            .name,
            "settings": schedule["settings"],
            "id": schedule["id"],
            "last_enabled_at": schedule["last_enabled_at"],
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
    ]
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
async def create_pipeline_schedules(
    uuid: str,
    data: schemas.PipelineScheduleCreate,
    db: Session,
    request: Request,
):
    exist_pipeline = (
        db.query(Pipeline)
        .filter(
            (Pipeline.id == uuid.replace("_", "-"))
            & (Pipeline.user_id == request.state.id)
        )
        .first()
    )
    if not exist_pipeline:
        return JSONResponse(
            content={"data": [], "message": "Pipeline không tồn tại"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    new_record = PipelineSchedule(
        name=data.name,
        pipeline_schedule_type=data.pipeline_schedule_type,
        pipeline_schedule_interval=data.pipeline_schedule_interval,
        pipeline_schedule_start_time=data.pipeline_schedule_start_time,
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    settings = data.settings
    description = data.description

    pipeline_schedule = {
        "pipeline_schedule": {
            "name": "schedule_"
            + unidecode(new_record.name.replace(" ", "_"))
            + "_"
            + str(new_record.id),
            "id": str(new_record.id),
            "description": description,
            "schedule_interval": new_record.pipeline_schedule_interval,
            "schedule_type": new_record.pipeline_schedule_type,
            "settings": settings,
            "start_time": new_record.pipeline_schedule_start_time,
        }
    }

    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/pipeline_schedules"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.post(url, json=pipeline_schedule, headers=headers)
    data_dict = response.json()
    if "error" not in data_dict:
        extracted_data = [
            {
                "name": new_record.name,
                "uuid": data_dict["pipeline_schedule"]["id"],
                "created_at": data_dict["pipeline_schedule"]["created_at"],
                "updated_at": data_dict["pipeline_schedule"]["updated_at"],
                "description": data_dict["pipeline_schedule"]["description"],
                "settings": data_dict["pipeline_schedule"]["settings"],
                "last_enabled_at": data_dict["pipeline_schedule"]["last_enabled_at"],
                "schedule_interval": data_dict["pipeline_schedule"][
                    "schedule_interval"
                ],
                "schedule_type": data_dict["pipeline_schedule"]["schedule_type"],
                "start_time": data_dict["pipeline_schedule"]["start_time"],
                "status": data_dict["pipeline_schedule"]["status"],
                "token": data_dict["pipeline_schedule"]["token"],
                # "variables": data_dict["pipeline_schedule"]["variables"],
            }
        ]
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": "",
                "message": "Tạo schedule thành công",
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
                "message": "Tạo schedule thất bại",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@handle_database_errors
async def update_pipeline_schedules(
    pipeline_schedules_uuid: str,
    data: schemas.PipelineScheduleUpdate,
    uuid: str,
    db: Session,
    request: Request,
):

    exist_pipeline = (
        db.query(Pipeline)
        .filter(
            (Pipeline.id == uuid.replace("_", "-"))
            & (Pipeline.user_id == request.state.id)
        )
        .first()
    )
    if not exist_pipeline:
        return JSONResponse(
            content={"data": [], "message": "Pipeline không tồn tại"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    exist_schedule = (
        db.query(PipelineSchedule)
        .filter(PipelineSchedule.id == pipeline_schedules_uuid.replace("_", "-"))
        .first()
    )
    if not exist_schedule:
        return JSONResponse(
            content={"data": [], "message": "Pipeline schedule không tồn tại"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if exist_schedule.pipeline_id != exist_pipeline.id:
        return JSONResponse(
            content={
                "data": [],
                "message": "Bạn không có quyền truy cập pipeline schedule này",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    settings = data.settings
    pipeline_schedule = {
        "pipeline_schedule": {
            "settings": settings
            # "tags": [tags],
        }
    }

    updated_schedule = {
        "pipeline_schedule": {
            "has_callback": True if data.has_callback else False,
            "retry_config": data.retry_config if data.has_callback else [],
        }
    }
    if data.schedule_type:
        updated_schedule["pipeline_schedule"]["schedule_type"] = data.schedule_type
    if data.description:
        updated_schedule["pipeline_schedule"]["description"] = data.description
    if data.schedule_interval:
        updated_schedule["pipeline_schedule"][
            "schedule_interval"
        ] = data.schedule_interval
    if data.start_time:
        updated_schedule["pipeline_schedule"]["start_time"] = data.start_time
    if data.status:
        updated_schedule["pipeline_schedule"]["status"] = data.status
    if data.name:
        updated_schedule["pipeline_schedule"]["name"] = (
            "schedule_"
            + unidecode(data.name.replace(" ", "_"))
            + "_"
            + str(exist_schedule.id)
        )

    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/pipeline_schedules/{pipeline_schedules_uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.post(url, json=pipeline_schedule, headers=headers)
    data_dict = response.json()
    if "error" not in data_dict:
        extracted_data = [
            {
                "name": exist_schedule.name,
                "created_at": data_dict["pipeline_schedule"]["created_at"],
                "updated_at": data_dict["pipeline_schedule"]["updated_at"],
                "description": data_dict["pipeline_schedule"]["description"],
                "settings": data_dict["pipeline_schedule"]["settings"],
                # "tags": data_dict["pipeline_schedule"]["tags"],
                "id": data_dict["pipeline_schedule"]["id"],
                "last_enabled_at": data_dict["pipeline_schedule"]["last_enabled_at"],
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
        ]
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": [],
                "message": "Sửa schedule thành công",
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
                "message": "Sửa schedule thất bại",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@handle_database_errors
async def delete_one_pipeline_schedules(
    uuid: str,
    pipeline_schedules_uuid: str,
    db: Session,
    request: Request,
):
    exist_pipeline = (
        db.query(Pipeline)
        .filter(
            (Pipeline.id == uuid.replace("_", "-"))
            & (Pipeline.user_id == request.state.id)
        )
        .first()
    )
    if not exist_pipeline:
        return JSONResponse(
            content={"data": [], "message": "Pipeline không tồn tại"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    exist_schedule = (
        db.query(PipelineSchedule)
        .filter(PipelineSchedule.id == pipeline_schedules_uuid.replace("_", "-"))
        .first()
    )
    if not exist_schedule:
        return JSONResponse(
            content={"data": [], "message": "Pipeline schedule không tồn tại"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if exist_schedule.pipeline_id != exist_pipeline.id:
        return JSONResponse(
            content={
                "data": [],
                "message": "Bạn không có quyền truy cập pipeline schedule này",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/pipeline_schedules/{pipeline_schedules_uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.delete(url, headers=headers)
    data_dict = response.json()
    if "error" not in data_dict:
        extracted_data = [
            {
                "name": exist_schedule.name,
                "created_at": data_dict["pipeline_schedule"]["created_at"],
                "updated_at": data_dict["pipeline_schedule"]["updated_at"],
                "description": data_dict["pipeline_schedule"]["description"],
                "settings": data_dict["pipeline_schedule"]["settings"],
                "id": data_dict["pipeline_schedule"]["id"],
                "last_enabled_at": data_dict["pipeline_schedule"]["last_enabled_at"],
                "schedule_interval": data_dict["pipeline_schedule"][
                    "schedule_interval"
                ],
                "schedule_type": data_dict["pipeline_schedule"]["schedule_type"],
                "start_time": data_dict["pipeline_schedule"]["start_time"],
                "status": data_dict["pipeline_schedule"]["status"],
                "token": data_dict["pipeline_schedule"]["token"],
                # "variables": data_dict["pipeline_schedule"]["variables"],
            }
        ]
        return JSONResponse(
            content={
                "data": extracted_data,
                "detail": [],
                "message": "Xóa schedule thành công",
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
                "message": "Xóa schedule thất bại",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
