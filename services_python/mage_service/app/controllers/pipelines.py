import os
from sqlalchemy.orm import Session
from fastapi import status, Request, UploadFile
from fastapi.responses import JSONResponse
import json
from services_python.mage_service.app.models import Pipeline, Block, PipelineSchedule
import services_python.mage_service.app.schemas.pipeline as schemas
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
    # db: Session,
    request: Request,
):
    user_id=request.state.id
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines?tag[]={user_id}"   # _limit=30&_offset=0
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.get(url, headers=headers)
    data_dict = response.json()

    # for pipeline in data_dict["pipelines"]:
    #     print("Pipeline:", pipeline["name"])
    #     print("Blocks:")
    #     for block in pipeline["blocks"]:
    #         print("- ", block["name"])
    #     print()

    extracted_data = {
        "pipelines": [],
        "metadata": {
            "count": data_dict["metadata"]["count"]
        }
    }

    # Iterate over each pipeline and extract required fields
    for pipeline in data_dict["pipelines"]:
        extracted_pipeline = {
            "created_at": pipeline.get("created_at"),
            "updated_at": pipeline.get("updated_at"),
            "description": pipeline.get("description"),
            "name": pipeline.get("name"),
            "settings": pipeline.get("settings"),
            "type": pipeline.get("type"),
            "uuid": pipeline.get("uuid"),
            "blocks_number": len(pipeline.get("blocks", [])),
            "schedules_number": len(pipeline.get("schedules", []))
        }
        extracted_data["pipelines"].append(extracted_pipeline)

    extracted_json = json.dumps(extracted_data)

    return JSONResponse(
        content=extracted_json,
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def get_one_pipeline(
    uuid: str,
    # db: Session,
    request: Request,
):
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.get(url, headers=headers)
    data_dict = response.json()

    extracted_data = {
        "pipelines": {
            "created_at": data_dict["pipeline"]["created_at"],
            "updated_at": data_dict["pipeline"]["updated_at"],
            "description": data_dict["pipeline"]["description"],
            "name": data_dict["pipeline"]["name"],
            "settings": data_dict["pipeline"]["settings"],
            "type": data_dict["pipeline"]["type"],
            "uuid": data_dict["pipeline"]["uuid"],
            "blocks": [{
                "name": block["name"],
                "downstream_blocks": block["downstream_blocks"],
                "type": block["type"],
                "upstream_blocks": block["upstream_blocks"],
                "uuid": block["uuid"],
                "status": block["status"],
                "conditional_blocks": block["conditional_blocks"],
                "callback_blocks": block["callback_blocks"],
                "has_callback": block["has_callback"],
                "retry_config": block["retry_config"]
            } for block in data_dict["pipeline"]["blocks"]]
        },
        "metadata": data_dict["metadata"]
    }
    extracted_json = json.dumps(extracted_data)
    return JSONResponse(
        content=extracted_json,
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def create_pipelines(
    data: schemas.PipelineCreate,
    # db: Session,
    request: Request,
):
    name = data.name
    type = data.type
    tags = request.state.id
    description = data.description

    if not name or not type:
        return JSONResponse(
            content={"error": "Name and type are required fields."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    extracted_info = {
        "pipeline": {
            "name": name,
            "type": type,
            "tags": tags,
            "description": description
        }
    }

    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.post(url, json=extracted_info, headers=headers)
    data_dict = response.json()
    pipeline=data_dict["pipeline"]
    extracted_pipeline = {
        "created_at": pipeline.get("created_at"),
        "updated_at": pipeline.get("updated_at"),
        "description": pipeline.get("description"),
        "name": pipeline.get("name"),
        "settings": pipeline.get("settings"),
        "type": pipeline.get("type"),
        # "uuid": pipeline.get("uuid"),
        # "variables_dir": pipeline.get("variables_dir"),
        "blocks_number": len(pipeline.get("blocks", [])),
        "schedules_number": len(pipeline.get("schedules", []))
    }
    extracted_data = {
        "pipelines": extracted_pipeline,
        "metadata": None
    }
    extracted_json = json.dumps(extracted_data)
    return JSONResponse(
        content=extracted_json,
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def delete_one_pipeline(
    uuid: str,
    # db: Session,
    request: Request,
):
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.delete(url, headers=headers)
    data_dict = response.json()
    pipeline=data_dict["pipeline"]
    extracted_pipeline = {
        "created_at": pipeline.get("created_at"),
        "updated_at": pipeline.get("updated_at"),
        "description": pipeline.get("description"),
        "name": pipeline.get("name"),
        "settings": pipeline.get("settings"),
        "tags": pipeline.get("tags"),
        "type": pipeline.get("type"),
        "uuid": pipeline.get("uuid"),
        "variables_dir": pipeline.get("variables_dir"),
        "blocks_number": len(pipeline.get("blocks", [])),
        "schedules_number": len(pipeline.get("schedules", []))
    }
    extracted_data = {
        "pipelines": extracted_pipeline,
        "metadata": None
    }
    extracted_json = json.dumps(extracted_data)
    return JSONResponse(
        content=extracted_json,
        status_code=status.HTTP_200_OK,
    )


# HANDLE BLOCKS

@handle_database_errors
def get_one_block(
    uuid: str,
    block_uuid: str,
    # db: Session,
    request: Request,
):
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/blocks/{block_uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.get(url, headers=headers)
    data_dict = response.json()
    extracted_data = {
        "blocks": {
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
            "content": data_dict["block"]["content"]
        },
        "metadata": data_dict["metadata"]
    }
    extracted_json = json.dumps(extracted_data)
    return JSONResponse(
        content=extracted_json,
        status_code=status.HTTP_200_OK,
    )


def get_block_content(block_type,source_type,config):
    if block_type == "data_loader":
        if source_type == "postgres":
            from services_python.mage_service.template.datasource.postgres import (
                get_string,
                check_config_keys,
            )
            if check_config_keys(config):
                return get_string(config)
        elif source_type == "mysql":
            pass
        elif source_type == "mongodb":
            pass
        elif source_type == "amazon_s3":
            pass
        else:
            pass


@handle_database_errors
def create_block(
    data: schemas.BlockCreate,
    uuid: str,
    # db: Session,
    request: Request,
):
    name = data.name
    source_type = data.source_type
    source_config = data.source_config
    block_type = data.block_type
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
    extracted_data = {
        "blocks": {
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
            "content": data_dict["block"]["content"]
        },
        "metadata": data_dict["metadata"]
    }
    extracted_json = json.dumps(extracted_data)
    return JSONResponse(
        content=extracted_json,
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def update_block(
    uuid: str,
    block_uuid: str,
    data: schemas.BlockUpdate,
    # db: Session,
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
    extracted_data = {
        "blocks": {
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
            "content": data_dict["block"]["content"]
        },
        "metadata": data_dict["metadata"]
    }
    extracted_json = json.dumps(extracted_data)
    return JSONResponse(
        content=extracted_json,
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def delete_one_block(
    uuid: str,
    block_uuid: str,
    # db: Session,
    request: Request,
):
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/blocks/{block_uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.delete(url, headers=headers)
    data_dict = response.json()
    extracted_data = {
        "blocks": {
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
            "content": data_dict["block"]["content"]
        },
        "metadata": data_dict["metadata"]
    }
    extracted_json = json.dumps(extracted_data)
    return JSONResponse(
        content=extracted_json,
        status_code=status.HTTP_200_OK,
    )


# HANDLE TRIGGERS

@handle_database_errors
def get_all_pipeline_schedules(
    uuid: str,
    # db: Session,
    request: Request,
):
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/pipeline_schedules"
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
                "pipeline_in_progress_runs_count": schedule["pipeline_in_progress_runs_count"],
                "pipeline_runs_count": schedule["pipeline_runs_count"]
            }
            for schedule in data_dict["pipeline_schedules"]
        ],
        "metadata": {
            "count": data_dict["metadata"]["count"]
        }
    }
    extracted_json = json.dumps(extracted_data)
    return JSONResponse(
        content=extracted_json,
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def create_pipeline_schedules(
    uuid: str,
    data: schemas.PipelineScheduleCreate,
    # db: Session,
    request: Request,
):
    name = data.name
    description = data.description
    schedule_interval = data.schedule_interval
    schedule_type = data.schedule_type
    settings = data.settings
    start_time = data.start_time
    tags = data.tags
    pipeline_schedule = {
        "pipeline_schedule": {
            "name": name,
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

    extracted_data = {
    "pipeline_schedules":{
        "created_at": data_dict["pipeline_schedules"]["created_at"],
        "updated_at": data_dict["pipeline_schedules"]["updated_at"],
        "description": data_dict["pipeline_schedules"]["description"],
        "name": data_dict["pipeline_schedules"]["name"],
        "settings": data_dict["pipeline_schedules"]["settings"],
        "tags": data_dict["pipeline_schedules"]["tags"],
        "id": data_dict["pipeline_schedules"]["id"],
        "last_enabled_at": data_dict["pipeline_schedules"]["last_enabled_at"],
        "pipeline_uuid": data_dict["pipeline_schedules"]["pipeline_uuid"],
        "schedule_interval": data_dict["pipeline_schedules"]["schedule_interval"],
        "schedule_type": data_dict["pipeline_schedules"]["schedule_type"],
        "start_time": data_dict["pipeline_schedules"]["start_time"],
        "status": data_dict["pipeline_schedules"]["status"],
        "token": data_dict["pipeline_schedules"]["token"],
        # "variables": data_dict["pipeline_schedules"]["variables"],
        "last_pipeline_run_status": data_dict["pipeline_schedules"]["last_pipeline_run_status"],
        "next_pipeline_run_date": data_dict["pipeline_schedules"]["next_pipeline_run_date"],
        "pipeline_in_progress_runs_count": data_dict["pipeline_schedules"]["pipeline_in_progress_runs_count"],
        "pipeline_runs_count": data_dict["pipeline_schedules"]["pipeline_runs_count"]
        },
    "metadata": data_dict["metadata"]
    }

    return JSONResponse(
        content=extracted_data,
        status_code=status.HTTP_200_OK,
    )

@handle_database_errors
def update_pipeline_schedules(
    pipeline_schedules_uuid: str,
    uuid: str,
    # db: Session,
    request: Request,
):
    data = request.json()
    name = data.get("name")
    description = data.get("description")
    schedule_interval = data.get("schedule_interval")
    schedule_type = data.get("schedule_type")
    settings = data.get("settings")
    start_time = data.get("start_time")
    my_status = data.get("status")
    tags = data.get("tags")
    pipeline_schedule = {
        "pipeline_schedule": {
            "name": name,
            "description": description,
            "schedule_interval": schedule_interval,
            "schedule_type": schedule_type,
            "settings": settings,
            "start_time": start_time,
            "status": my_status,
            "tags": tags,
        }
    }

    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/pipeline_schedules/{pipeline_schedules_uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.post(url, json=pipeline_schedule, headers=headers)
    data_dict = response.json()

    extracted_data = {
    "pipeline_schedules":{
        "created_at": data_dict["pipeline_schedules"]["created_at"],
        "updated_at": data_dict["pipeline_schedules"]["updated_at"],
        "description": data_dict["pipeline_schedules"]["description"],
        "name": data_dict["pipeline_schedules"]["name"],
        "settings": data_dict["pipeline_schedules"]["settings"],
        "tags": data_dict["pipeline_schedules"]["tags"],
        "id": data_dict["pipeline_schedules"]["id"],
        "last_enabled_at": data_dict["pipeline_schedules"]["last_enabled_at"],
        "pipeline_uuid": data_dict["pipeline_schedules"]["pipeline_uuid"],
        "schedule_interval": data_dict["pipeline_schedules"]["schedule_interval"],
        "schedule_type": data_dict["pipeline_schedules"]["schedule_type"],
        "start_time": data_dict["pipeline_schedules"]["start_time"],
        "status": data_dict["pipeline_schedules"]["status"],
        "token": data_dict["pipeline_schedules"]["token"],
        # "variables": data_dict["pipeline_schedules"]["variables"],
        "last_pipeline_run_status": data_dict["pipeline_schedules"]["last_pipeline_run_status"],
        "next_pipeline_run_date": data_dict["pipeline_schedules"]["next_pipeline_run_date"],
        "pipeline_in_progress_runs_count": data_dict["pipeline_schedules"]["pipeline_in_progress_runs_count"],
        "pipeline_runs_count": data_dict["pipeline_schedules"]["pipeline_runs_count"]
        },
    "metadata": data_dict["metadata"]
    }

    return JSONResponse(
        content=extracted_data,
        status_code=status.HTTP_200_OK,
    )

@handle_database_errors
def delete_one_pipeline_schedules(
    uuid: str,
    pipeline_schedules_uuid: str,
    # db: Session,
    request: Request,
):
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/pipeline_schedules/{pipeline_schedules_uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.delete(url, headers=headers)
    data_dict = response.json()
    extracted_data = {
    "pipeline_schedules":{
        "created_at": data_dict["pipeline_schedules"]["created_at"],
        "updated_at": data_dict["pipeline_schedules"]["updated_at"],
        "description": data_dict["pipeline_schedules"]["description"],
        "name": data_dict["pipeline_schedules"]["name"],
        "settings": data_dict["pipeline_schedules"]["settings"],
        "tags": data_dict["pipeline_schedules"]["tags"],
        "id": data_dict["pipeline_schedules"]["id"],
        "last_enabled_at": data_dict["pipeline_schedules"]["last_enabled_at"],
        "pipeline_uuid": data_dict["pipeline_schedules"]["pipeline_uuid"],
        "schedule_interval": data_dict["pipeline_schedules"]["schedule_interval"],
        "schedule_type": data_dict["pipeline_schedules"]["schedule_type"],
        "start_time": data_dict["pipeline_schedules"]["start_time"],
        "status": data_dict["pipeline_schedules"]["status"],
        "token": data_dict["pipeline_schedules"]["token"],
        # "variables": data_dict["pipeline_schedules"]["variables"],
        "last_pipeline_run_status": data_dict["pipeline_schedules"]["last_pipeline_run_status"],
        "next_pipeline_run_date": data_dict["pipeline_schedules"]["next_pipeline_run_date"],
        "pipeline_in_progress_runs_count": data_dict["pipeline_schedules"]["pipeline_in_progress_runs_count"],
        "pipeline_runs_count": data_dict["pipeline_schedules"]["pipeline_runs_count"]
        },
    "metadata": data_dict["metadata"]
    }

    return JSONResponse(
        content=extracted_data,
        status_code=status.HTTP_200_OK,
    )
