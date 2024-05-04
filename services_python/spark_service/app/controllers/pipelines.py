import os
from sqlalchemy.orm import Session
from fastapi import status, Request, UploadFile
from fastapi.responses import JSONResponse

from services_python.data_service.app.models import Dataset
import services_python.data_service.app.schemas.datamarts as schemas
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
    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.get(url, headers=headers)
    data_dict = response.json()

    for pipeline in data_dict["pipelines"]:
        print("Pipeline:", pipeline["name"])
        print("Blocks:")
        for block in pipeline["blocks"]:
            print("- ", block["name"])
        print()

    return JSONResponse(
        content=data_dict,
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
    pipeline_name = data_dict["pipeline"]["name"]
    pipeline_blocks = data_dict["pipeline"]["blocks"]
    pipeline_updated_at = data_dict["pipeline"]["updated_at"]

    # Print extracted information
    print("Pipeline Name:", pipeline_name)
    print("Pipeline Updated At:", pipeline_updated_at)
    print("Pipeline Blocks:")
    for block in pipeline_blocks:
        print("Block Name:", block["name"])
        print("Block Type:", block["type"])
        print("Block Status:", block["status"])
        print("Block Content:", block["content"])
        print("-----------")
    return JSONResponse(
        content=data_dict,
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def create_pipelines(
    # db: Session,
    request: Request,
):

    data = request.json()
    name = data.get("name")
    type = data.get("type")
    clone_pipeline_uuid = data.get("clone_pipeline_uuid")
    extensions = data.get("extensions")
    callbacks = data.get("callbacks")
    conditionals = data.get("conditionals")

    extracted_info = {
        "pipeline": {
            "name": name,
            "type": type,
            "clone_pipeline_uuid": clone_pipeline_uuid,
            "extensions": extensions,
            "callbacks": callbacks,
            "conditionals": conditionals,
        }
    }

    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.post(url, json=extracted_info, headers=headers)
    data_dict = response.json()

    return JSONResponse(
        content=data_dict,
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
    return JSONResponse(
        content=data_dict,
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
    return JSONResponse(
        content=data_dict,
        status_code=status.HTTP_200_OK,
    )


def get_data_source_block_content(type, config):
    if type == "postgres":
        from services_python.mage_service.template.datasource.postgres import (
            get_string,
            check_config_keys,
        )

        if check_config_keys(config):
            return get_string(config)
    elif type == "mysql":
        pass
    elif type == "mongodb":
        pass
    elif type == "amazon_s3":
        pass
    else:
        pass


@handle_database_errors
def create_data_source_block(
    uuid: str,
    # db: Session,
    request: Request,
):
    data = request.json()
    name = data.get("name")
    block_type = data.get("type")
    code_config = data.get("config")
    content = get_data_source_block_content(block_type, code_config)
    # color = data.get("color")
    # configuration = data.get("configuration")
    # extension_uuid = data.get("extension_uuid")
    # pipelines = data.get("pipelines")
    # priority = data.get("priority")
    # upstream_blocks = data.get("upstream_blocks")
    # block_uuid = data.get("block_uuid") #                 Optional
    language = "python"
    type = "data_loader"
    extracted_info = {
        "block": {
            "name": name,
            "type": type,
            "content": content,
            "language": language,
            # "color": color,
            # "config": config,
            # "configuration": configuration,
            # "extension_uuid": extension_uuid,
            # "pipelines": pipelines,
            # "priority": priority,
            # "upstream_blocks": upstream_blocks
            # "uuid": block_uuid
        }
    }

    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/blocks"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.post(url, json=extracted_info, headers=headers)
    data_dict = response.json()
    data_dict = response.json()
    return JSONResponse(
        content=data_dict,
        status_code=status.HTTP_200_OK,
    )


handle_database_errors


def update_block(
    uuid: str,
    block_uuid: str,
    # db: Session,
    request: Request,
):
    data = request.json()
    name = data.get("name")
    block_type = data.get("type")
    bookmark_values = data.get("bookmark_values")
    callback_blocks = data.get("callback_blocks")
    color = data.get("color")
    configuration = data.get("configuration")
    content = data.get("content")
    destination_table = data.get("destination_table")
    downstream_blocks = data.get("downstream_blocks")
    executor_config = data.get("executor_config")
    executor_type = data.get("executor_type")
    extension_uuid = data.get("extension_uuid")
    language = data.get("language")
    pipelines = data.get("pipelines")
    retry_config = data.get("retry_config")
    tap_stream_id = data.get("tap_stream_id")
    upstream_blocks = data.get("upstream_blocks")

    updated_block = {
        "block": {
            "name": name,
            "type": block_type,
            "bookmark_values": bookmark_values,
            "callback_blocks": callback_blocks,
            "color": color,
            "configuration": configuration,
            "content": content,
            "destination_table": destination_table,
            "downstream_blocks": downstream_blocks,
            "executor_config": executor_config,
            "executor_type": executor_type,
            "extension_uuid": extension_uuid,
            "language": language,
            "pipelines": pipelines,
            "retry_config": retry_config,
            "tap_stream_id": tap_stream_id,
            "upstream_blocks": upstream_blocks,
        }
    }

    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/blocks/{block_uuid}"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.put(url, json=updated_block, headers=headers)
    data_dict = response.json()
    return JSONResponse(
        content=data_dict,
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
    return JSONResponse(
        content=data_dict,
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
    return JSONResponse(
        content=data_dict,
        status_code=status.HTTP_200_OK,
    )


@handle_database_errors
def create_pipeline_schedules(
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
    sla = data.get("sla")
    start_time = data.get("start_time")
    my_status = data.get("status")
    variables = data.get("variables")

    pipeline_schedule = {
        "pipeline_schedule": {
            "name": name,
            "description": description,
            "schedule_interval": schedule_interval,
            "schedule_type": schedule_type,
            "settings": settings,
            "sla": sla,
            "start_time": start_time,
            "status": my_status,
            "variables": variables,
        }
    }

    url = f"http://{MAGE_HOST}:{MAGE_PORT}/api/pipelines/{uuid}/pipeline_schedules"
    headers = {"x_api_key": MAGE_API_KEY}
    response = requests.post(url, json=pipeline_schedule, headers=headers)
    data_dict = response.json()
    return JSONResponse(
        content=data_dict,
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
    return JSONResponse(
        content=data_dict,
        status_code=status.HTTP_200_OK,
    )
