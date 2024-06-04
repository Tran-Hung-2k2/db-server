from fastapi import APIRouter, Request, Depends
from services_python.ml_service.app import schemas
from services_python.ml_service.app import controller as ctl
from services_python.ml_service.app.database import get_session

from sqlalchemy.orm import Session

router = APIRouter(prefix="/projects/{project_id}/runs", tags=["Runs"])


@router.post("/", summary="Create a run from project")
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


@router.get("/", summary="Get list of runs from project")
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
