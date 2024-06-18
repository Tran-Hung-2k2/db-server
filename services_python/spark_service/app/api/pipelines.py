import json
from pydantic import UUID4
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile

import services_python.spark_service.app.controllers.pipelines as ctl
import services_python.spark_service.app.schemas.pipelines as schemas
import services_python.middlewares.auth as middlewares
from services_python.spark_service.app.database import get_session

router = APIRouter(prefix="/pipelines", tags=["Pipelines"])

# ROUTES FOR PIPELINES


@router.get("/", dependencies=[Depends(middlewares.verify_all)])
async def get_all_pipelines(
    request: Request,
    db: Session = Depends(get_session),
):

    return await ctl.get_all_pipelines(
        db=db,
        request=request
    )


@router.get("/{uuid}", dependencies=[Depends(middlewares.verify_all)])
async def get_one_pipeline(
    uuid: str,
    request: Request,
    db: Session = Depends(get_session),
):
    return await ctl.get_one_pipeline(
        uuid=uuid,
        db=db,
        request=request,
    )


@router.post("/", dependencies=[Depends(middlewares.verify_user)])
async def create_pipelines(
    request: Request,
    data: schemas.PipelineCreate,
    db: Session = Depends(get_session),
):
    return await ctl.create_pipelines(
        db=db,
        data=data,
        request=request,
    )

@router.patch("/{uuid}", dependencies=[Depends(middlewares.verify_all)])
async def update_pipeline(
    uuid: str,
    data: schemas.PipelineUpdate,
    request: Request,
    db: Session = Depends(get_session),
):
    return await ctl.update_pipeline(
        uuid=uuid,
        data=data,
        db=db,
        request=request,
    )

@router.delete("/{uuid}", dependencies=[Depends(middlewares.verify_user)])
async def delete_one_pipeline(
    request: Request,
    uuid: str,
    db: Session = Depends(get_session)
):
    return await ctl.delete_one_pipeline(
        db=db,
        uuid=uuid,
        request=request,
    )


# ROUTES FOR BLOCKS


@router.get(
    "/{uuid}/blocks/{block_uuid}", dependencies=[Depends(middlewares.verify_all)]
)
async def get_one_block(
    uuid: str,
    block_uuid: str,
    request: Request,
    db: Session = Depends(get_session),
):
    return await ctl.get_one_block(
        uuid=uuid,
        block_uuid=block_uuid,
        db=db,
        request=request,
    )


@router.post(
    "/{uuid}/blocks", dependencies=[Depends(middlewares.verify_user)]
)
async def create_block(
    uuid: str,
    request: Request,
    data: schemas.BlockCreate,
    db: Session = Depends(get_session),
):
    return await ctl.create_block(
        uuid=uuid,
        db=db,
        data=data,
        request=request,
    )


@router.patch(
    "/{uuid}/blocks/{block_uuid}", dependencies=[Depends(middlewares.verify_user)]
)
async def update_block(
    request: Request,
    uuid: str,
    block_uuid: str,
    data: schemas.BlockUpdate,
    db: Session = Depends(get_session),
):
    return await ctl.update_block(
        db=db,
        uuid=uuid,
        block_uuid=block_uuid,
        data=data,
        request=request,
    )


@router.delete(
    "/{uuid}/blocks/{block_uuid}", dependencies=[Depends(middlewares.verify_user)]
)
async def delete_one_block(
    request: Request,
    uuid: str,
    block_uuid: str,
    db: Session = Depends(get_session)
):
    return await ctl.delete_one_block(
        db=db,
        uuid=uuid,
        block_uuid=block_uuid,
        request=request,
    )


# ROUTES FOR TRIGGER


@router.get(
    "/{uuid}/pipeline_schedules", dependencies=[Depends(middlewares.verify_all)]
)
async def get_all_pipeline_schedules(
    uuid: str,
    request: Request,
    db: Session = Depends(get_session),
):
    return await ctl.get_all_pipeline_schedules(
        uuid=uuid,
        db=db,
        request=request,
    )


@router.post(
    "/{uuid}/pipeline_schedules", dependencies=[Depends(middlewares.verify_user)]
)
async def create_pipeline_schedules(
    uuid: str,
    request: Request,
    data: schemas.PipelineScheduleCreate,
    db: Session = Depends(get_session),
):
    return await ctl.create_pipeline_schedules(
        uuid=uuid,
        db=db,
        data=data,
        request=request,
    )


@router.patch(
    "/{uuid}/pipeline_schedules/{pipeline_schedules_uuid}",
    dependencies=[Depends(middlewares.verify_user)],
)
async def update_pipeline_schedules(
    uuid: str,
    pipeline_schedules_uuid: str,
    request: Request,
    data: schemas.PipelineUpdate,
    db: Session = Depends(get_session),
):
    return await ctl.update_pipeline_schedules(
        uuid=uuid,
        pipeline_schedules_uuid=pipeline_schedules_uuid,
        db=db,
        data=data,
        request=request,
    )


@router.delete(
    "/{uuid}/pipeline_schedules/{pipeline_schedules_uuid}",
    dependencies=[Depends(middlewares.verify_user)],
)
async def delete_one_pipeline_schedules(
    request: Request,
    uuid: str,
    pipeline_schedules_uuid: str,
    db: Session = Depends(get_session)
):
    return await ctl.delete_one_pipeline_schedules(
        db=db,
        uuid=uuid,
        pipeline_schedules_uuid=pipeline_schedules_uuid,
        request=request,
    )
