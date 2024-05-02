from fastapi import APIRouter

from services_python.data_service.app.api.v1.datamarts import router as dataset_router

router = APIRouter(prefix="/api")
router.include_router(dataset_router)
