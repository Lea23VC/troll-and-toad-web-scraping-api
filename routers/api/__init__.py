from fastapi import APIRouter
from .v1.search import router as v1_api_router

router = APIRouter()
router.include_router(v1_api_router, prefix="/v1", tags=["v1"])
