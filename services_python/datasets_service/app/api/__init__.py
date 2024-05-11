from fastapi import APIRouter

from services_python.datasets_service.app.api.datasets import router as dataset_router

router = APIRouter(prefix="/api")
router.include_router(dataset_router)
