import json
from pydantic import UUID4
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile

import services_python.mage_service.app.controllers.template as ctl
import services_python.mage_service.app.schemas.pipelines as schemas
import services_python.middlewares.auth as middlewares
from services_python.mage_service.app.database import get_session

router = APIRouter(prefix="/pipelines_schedules", tags=["Pipelines_schedules"])

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
    "/"
    # , dependencies=[Depends(middlewares.verify_user)]
)
async def create_block(
    request: Request,
    data: schemas.DatasetCreate,
    # db: Session = Depends(get_session),
):
    return ctl.create_block(
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
