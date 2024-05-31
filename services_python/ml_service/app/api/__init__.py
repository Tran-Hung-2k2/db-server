from fastapi import APIRouter

from .projects import router as project_router
from .runs import router as run_router


router = APIRouter(prefix="/api/ml")
router.include_router(project_router)
router.include_router(run_router)
