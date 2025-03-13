"""Routes package for Dell Unisphere API.

This package contains the API endpoints for the Dell Unisphere API.
"""

from fastapi import APIRouter

from .system import router as system_router
from .auth import router as auth_router
from .upgrade import router as upgrade_router
from .upload import router as upload_router
from .software import router as software_router

router = APIRouter()
router.include_router(system_router)
router.include_router(auth_router)
router.include_router(upgrade_router)
router.include_router(upload_router)
router.include_router(software_router)

__all__ = ["router"]
