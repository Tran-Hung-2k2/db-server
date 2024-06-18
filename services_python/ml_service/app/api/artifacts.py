from fastapi import APIRouter, Request, Depends
from services_python.ml_service.app.controller import artifacts as ctl
from services_python.ml_service.app.database import get_session

from sqlalchemy.orm import Session

router = APIRouter(prefix="/artifacts", tags=["Artifacts"])


@router.get("/{run_id}", summary="Get list of artifacts")
async def search_artifact(
    run_id: str,
    request: Request,
    db: Session = Depends(get_session),
):
    return await ctl.search_artifact(
        run_id=run_id,
        request=request,
        db=db,
    )


@router.get("/{run_id}/get", summary="Get list of models")
async def get_artifact(
    run_id: str,
    request: Request,
    db: Session = Depends(get_session),
):
    return await ctl.get_artifact(
        run_id=run_id,
        request=request,
        db=db,
    )
