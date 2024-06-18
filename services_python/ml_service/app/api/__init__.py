from fastapi import APIRouter

from .projects import router as project_router
from .runs import router as run_router
from .ml_models import router as model_router
from .artifacts import router as artifact_router

router = APIRouter(prefix="/api/mlops", tags=["MLOps API"])
router.include_router(project_router)
router.include_router(run_router)
router.include_router(model_router)
router.include_router(artifact_router)
