import os
from sqlalchemy.orm import Session
from fastapi import status, Request, UploadFile
from fastapi.responses import JSONResponse

from services_python.data_service.app.models import Dataset
import services_python.data_service.app.schemas.datasets as schemas
from services_python.utils.exception import MyException
import services_python.constants.label as label
from services_python.utils.handle_errors_wrapper import handle_database_errors
# from services_python.utils.delta import (
#     save_file_to_s3_as_delta,
#     query_sql_from_delta_table,
# )

import requests # type: ignore
LIMIT_RECORD = int(os.getenv("LIMIT_RECORD", "50"))

# import constants
from services_python.mage_service.constants import HOST, PORT, API_KEY


# HANDLE PIPELINES RUNS

@handle_database_errors
def get_all_runs(
    db: Session, 
    request: Request):
    url = f"http://{HOST}:{PORT}/api/pipelines"
    headers = {"x_api_key": API_KEY}
    response = requests.get(url, headers=headers)
    data_dict = response.json()
    return JSONResponse(
        content=data_dict,
        status_code=status.HTTP_200_OK,
    )

# @handle_database_errors
# def get_one_pipelines(
#     uuid: str,
#     db: Session, 
#     request: Request):
#     url = f"http://{HOST}:{PORT}/api/pipelines_schedules/{uuid}/pipelines_runs"
#     headers = {"x_api_key": API_KEY}
#     response = requests.get(url, headers=headers)
#     data_dict = response.json()
#     return JSONResponse(
#         content=data_dict,
#         status_code=status.HTTP_200_OK,
#     )

# @handle_database_errors
# def create_pipelines(
#     db: Session, 
#     request: Request):

#     data = request.json()
#     name = data.get("name")
#     type = data.get("type")
#     clone_pipeline_uuid = data.get("clone_pipeline_uuid")
#     extensions = data.get("extensions")
#     callbacks = data.get("callbacks")
#     conditionals = data.get("conditionals")

#     extracted_info = {
#         "pipeline": {
#             "name": name,
#             "type": type,
#             "clone_pipeline_uuid": clone_pipeline_uuid,
#             "extensions": extensions,
#             "callbacks": callbacks,
#             "conditionals": conditionals
#         }
#     }

#     url = f"http://{HOST}:{PORT}/api/pipelines"
#     headers = {"x_api_key": API_KEY}
#     response = requests.post(url, json=extracted_info, headers=headers)
#     data_dict = response.json()

#     return JSONResponse(
#         content=data_dict,
#         status_code=status.HTTP_200_OK,
#     )

# @handle_database_errors
# def delete_one_pipeline(
#     uuid: str,
#     db: Session, 
#     request: Request):
#     url = f"http://{HOST}:{PORT}/api/pipelines/{uuid}"
#     headers = {"x_api_key": API_KEY}
#     response = requests.delete(url, headers=headers)
#     data_dict = response.json()
#     return JSONResponse(
#         content=data_dict,
#         status_code=status.HTTP_200_OK,
#     )