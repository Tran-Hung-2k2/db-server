from fastapi import APIRouter, Request, Depends
from services_python.ml_service.app import schemas
from services_python.ml_service.app import controller as ctl
from services_python.ml_service.app.database import get_session

from sqlalchemy.orm import Session

router = APIRouter(prefix="/projects/{project_id}/runs", tags=["Runs"])


@router.post("/", summary="Create a run from a project")
async def create_run(
    project_id: str,
    request: Request,
    data: schemas.RunCreate,
    db: Session = Depends(get_session),
):
    return await ctl.create_run(
        project_id=project_id,
        request=request,
        data=data,
        db=db,
    )


@router.get("/", summary="Get list of runs from a project")
async def search_run(
    project_id: str,
    request: Request,
    db: Session = Depends(get_session),
):
    return await ctl.search_run(
        project_id=project_id,
        request=request,
        db=db,
    )


@router.get("/{run_id}", summary="Get run from run_id")
async def get_run(
    project_id: str,
    run_id: str,
    request: Request,
    db: Session = Depends(get_session),
):
    return await ctl.get_run(
        project_id=project_id,
        run_id=run_id,
        request=request,
        db=db,
    )


@router.delete("/{run_id}", summary="Delete a run")
async def delete_run(
    project_id: str,
    run_id: str,
    request: Request,
    db: Session = Depends(get_session),
):
    return await ctl.delete_run(
        project_id=project_id,
        run_id=run_id,
        request=request,
        db=db,
    )


@router.patch("/{run_id}", summary="Update a run")
async def update_run(
    project_id: str,
    run_id: str,
    request: Request,
    data: schemas.ProjectUpdate,
    db: Session = Depends(get_session),
):
    return await ctl.update_run(
        project_id=project_id,
        run_id=run_id,
        request=request,
        data=data,
        db=db,
    )
