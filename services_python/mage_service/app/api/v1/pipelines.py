import json
from pydantic import UUID4
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile

import services_python.mage_service.app.controllers.pipelines as ctl
import services_python.mage_service.app.schemas.datasets as schemas
import services_python.middlewares.auth as middlewares
from services_python.mage_service.app.database import get_session

router = APIRouter(prefix="/pipelines", tags=["Pipelines"])

# ROUTES FOR PIPELINES


@router.get(
    "/"
    # , dependencies=[Depends(middlewares.verify_all)]
)
async def get_all_pipelines(
    request: Request,
    # db: Session = Depends(get_session),
):

    return ctl.get_all_pipelines(
        # db,
        request
    )


@router.get(
    "/{uuid}"
    # , dependencies=[Depends(middlewares.verify_all)]
)
async def get_one_pipeline(
    uuid: str,
    request: Request,
    # db: Session = Depends(get_session),
):
    return ctl.get_one_pipeline(
        uuid,
        # db,
        request,
    )


@router.post(
    "/"
    # , dependencies=[Depends(middlewares.verify_user)]
)
async def create_pipelines(
    request: Request,
    data: schemas.DatasetCreate,
    # db: Session = Depends(get_session),
):
    return ctl.create_pipelines(
        # db,
        data,
        request,
    )


@router.delete(
    "/{uuid}"
    # , dependencies=[Depends(middlewares.verify_user)]
)
async def delete_one_pipeline(
    request: Request,
    uuid: str,
    # db: Session = Depends(get_session)
):
    return ctl.delete_one_pipeline(
        # db,
        uuid,
        request,
    )


# ROUTES FOR BLOCKS


@router.get(
    "/{uuid}/blocks/{block_uuid}"
    # , dependencies=[Depends(middlewares.verify_all)]
)
async def get_one_block(
    uuid: str,
    block_uuid: str,
    request: Request,
    # db: Session = Depends(get_session),
):
    return ctl.get_one_block(
        uuid,
        block_uuid,
        # db,
        request,
    )


@router.post(
    "/{uuid}/blocks/datasource"
    # , dependencies=[Depends(middlewares.verify_user)]
)
async def create_data_source_block(
    uuid: str,
    request: Request,
    data: schemas.DatasetCreate,
    # db: Session = Depends(get_session),
):
    return ctl.create_data_source_block(
        uuid,
        # db,
        data,
        request,
    )


@router.put(
    "/{uuid}/blocks/{block_uuid}"
    # , dependencies=[Depends(middlewares.verify_user)]
)
async def update_block(
    request: Request,
    uuid: str,
    block_uuid: str,
    data: schemas.DatasetCreate,
    # db: Session = Depends(get_session),
):
    return ctl.update_block(
        # db,
        uuid,
        block_uuid,
        data,
        request,
    )


@router.delete(
    "/{uuid}/blocks/{block_uuid}"
    # , dependencies=[Depends(middlewares.verify_user)]
)
async def delete_one_block(
    request: Request,
    uuid: str,
    block_uuid: str,
    # db: Session = Depends(get_session)
):
    return ctl.delete_one_block(
        # db,
        uuid,
        block_uuid,
        request,
    )


# ROUTES FOR TRIGGER


@router.get(
    "/{uuid}/pipeline_schedules"
    # , dependencies=[Depends(middlewares.verify_all)]
)
async def get_all_pipeline_schedules(
    uuid: str,
    request: Request,
    # db: Session = Depends(get_session),
):
    return ctl.get_all_pipeline_schedules(
        uuid,
        # db,
        request,
    )


@router.post(
    "/{uuid}/pipeline_schedules"
    # , dependencies=[Depends(middlewares.verify_user)]
)
async def create_pipeline_schedules(
    request: Request,
    data: schemas.DatasetCreate,
    # db: Session = Depends(get_session),
):
    return ctl.create_pipeline_schedules(
        # db,
        data,
        request,
    )


@router.delete(
    "/{uuid}/pipeline_schedules/{pipeline_schedules_uuid}"
    # , dependencies=[Depends(middlewares.verify_user)]
)
async def delete_one_pipeline_schedules(
    request: Request,
    uuid: str,
    pipeline_schedules_uuid: str,
    # db: Session = Depends(get_session)
):
    return ctl.delete_one_pipeline_schedules(
        # db,
        uuid,
        pipeline_schedules_uuid,
        request,
    )
