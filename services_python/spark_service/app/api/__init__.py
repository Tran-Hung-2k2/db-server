from fastapi import APIRouter

from services_python.spark_service.app.api.pipelines import router as pipelines_router

router = APIRouter(prefix="/spark")
router.include_router(pipelines_router)
