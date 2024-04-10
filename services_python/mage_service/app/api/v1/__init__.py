from fastapi import APIRouter

from services_python.mage_service.app.api.v1.pipelines import router as dataset_router

router = APIRouter(prefix="/mage")
router.include_router(dataset_router)
