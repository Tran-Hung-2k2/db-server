from fastapi import APIRouter, Request, Depends
from services_python.ml_service.app.schemas import projects as schemas
from services_python.ml_service.app.controller import projects as ctl
from services_python.ml_service.app.database import get_session

from sqlalchemy.orm import Session

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", summary="Create a project with name")
async def create_project(
    data: schemas.ProjectCreate,
    request: Request,
    db: Session = Depends(get_session),
):
    return await ctl.create_project(
        data=data,
        request=request,
        db=db,
    )


@router.get("/", summary="Get list of projects")
async def search_project(
    request: Request,
    db: Session = Depends(get_session),
):
    return await ctl.search_project(
        request=request,
        db=db,
    )


@router.delete("/{id}", summary="Delete a project")
async def delete_project(
    id: str,
    request: Request,
    db: Session = Depends(get_session),
):
    return await ctl.delete_project(
        id=id,
        request=request,
        db=db,
    )


@router.patch("/{id}", summary="Update a project")
async def update_project(
    id: str,
    data: schemas.ProjectUpdate,
    request: Request,
    db: Session = Depends(get_session),
):
    return await ctl.update_project(
        id=id,
        data=data,
        request=request,
        db=db,
    )


@router.post("/{id}", summary="Config a project")
async def config_project(
    id: str,
    data: schemas.ProjectConfig,
    request: Request,
    db: Session = Depends(get_session),
):
    return await ctl.config_project(
        id=id,
        data=data,
        request=request,
        db=db,
    )
