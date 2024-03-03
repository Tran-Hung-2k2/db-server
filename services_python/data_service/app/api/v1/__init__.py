from fastapi import APIRouter

from services_python.data_service.app.api.v1.datasets import router as dataset_router
from services_python.data_service.app.api.v1.datasources import (
    router as datasource_router,
)

router = APIRouter(prefix="/api/v1")
router.include_router(dataset_router)
router.include_router(datasource_router)
