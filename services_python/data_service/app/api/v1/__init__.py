from fastapi import APIRouter

from api.v1.datasets import router as dataset_router

router = APIRouter(prefix="/api/v1")
router.include_router(dataset_router)
