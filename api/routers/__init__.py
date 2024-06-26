from fastapi import APIRouter
from .glassnet_router import router as glassnet_router
from .viscnet_router import router as viscnet_router
# from .sciglassdata_router import router as sciglassdata_router

router = APIRouter()
router.include_router(glassnet_router, tags=["GlassNet"])
# router.include_router(viscnet_router, tags=["ViscNet"])
# router.include_router(sciglassdata_router, tags=["SciglassData"])