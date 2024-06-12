from fastapi import APIRouter
from .glassnet_router import router as glassnet_router
from .viscnet_router import router as viscnet_router
from .sciglassdata_router import router as sciglassdata_router

api_router = APIRouter()

api_router.include_router(glassnet_router, prefix="/glassnet12", tags=["GlassNet"])
api_router.include_router(viscnet_router, prefix="/viscnet", tags=["ViscNet"])
api_router.include_router(sciglassdata_router, prefix="/sciglassdata", tags=["SciglassData"])