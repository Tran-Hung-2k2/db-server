from fastapi import APIRouter, Request, Depends
from services_python.ml_service.app.schemas import ml_models as schemas
from services_python.ml_service.app.controller import ml_models as ctl
from services_python.ml_service.app.database import get_session

from sqlalchemy.orm import Session

router = APIRouter(prefix="/models", tags=["Models"])


@router.get("/", summary="Get list of models")
async def search_model(
    request: Request,
    db: Session = Depends(get_session),
):
    return await ctl.search_model(
        request=request,
        db=db,
    )


@router.get("/{project_id}", summary="Get list of model versions")
async def search_model_version(
    project_id: str,
    request: Request,
    db: Session = Depends(get_session),
):
    return await ctl.search_model_version(
        project_id=project_id,
        request=request,
        db=db,
    )


@router.get("/{project_id}/versions/{version}", summary="Get model version")
async def get_model_version(
    project_id: str,
    version: str,
    request: Request,
    db: Session = Depends(get_session),
):
    return await ctl.get_model_version(
        project_id=project_id,
        version=version,
        request=request,
        db=db,
    )
