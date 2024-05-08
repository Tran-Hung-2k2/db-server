from fastapi import APIRouter

from services_python.mage_service.app.api.pipelines import router as pipelines_router

router = APIRouter(prefix="/api")
router.include_router(pipelines_router)
