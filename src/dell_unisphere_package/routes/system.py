"""System routes for Dell Unisphere API.

This module defines the API endpoints for system information.
"""

from fastapi import APIRouter, Request

from ..controllers.auth import format_response
from ..schemas.base import BasicSystemInfo

router = APIRouter(prefix="/api")

FullVersion = "Unity 5.3.0.0 (Release, Build 120, 2023-03-18 19:02:01, 5.3.0.0.5.120)"


@router.get("/types/basicSystemInfo/instances")
def get_basic_system_info(request: Request):
    """Get basic system information."""
    system_info = BasicSystemInfo()
    return format_response([system_info], request, instance_type="basicSystemInfo")
