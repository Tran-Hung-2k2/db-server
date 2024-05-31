from fastapi import APIRouter

from services_python.mage_service.app.api.v1.pipelines import router as pipelines_router

router = APIRouter(prefix="/datamart")
router.include_router(pipelines_router)
