from fastapi import APIRouter

from api.v1.datasource_types import router as datasource_type_router
from api.v1.datasources import router as datasource_router
from api.v1.datasets import router as dataset_router

router = APIRouter(prefix="/api/v1")
router.include_router(datasource_type_router)
router.include_router(datasource_router)
router.include_router(dataset_router)
