"""System routes for Dell Unisphere API.

This module defines the API endpoints for system information.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from ..controllers.auth import format_response, get_current_user
from ..models.storage import system_config
from ..schemas.base import BasicSystemInfo

router = APIRouter(prefix="/api")

FullVersion = "Unity 5.3.0.0 (Release, Build 120, 2023-03-18 19:02:01, 5.3.0.0.5.120)"


# Define models for system configuration
class SystemConfigUpdate(BaseModel):
    """Model for updating system configuration."""

    eligibility_status: Optional[str] = None  # 'success', 'failure', or 'auto'
    failure_codes: Optional[List[str]] = None
    auto_failure_threshold: Optional[float] = None


@router.get("/types/basicSystemInfo/instances")
def get_basic_system_info(request: Request):
    """Get basic system information."""
    system_info = BasicSystemInfo()
    return format_response([system_info], request, instance_type="basicSystemInfo")


@router.get("/types/systemConfig/instances")
def get_system_config(request: Request, current_user=Depends(get_current_user)):
    """Get current system configuration for testing."""
    return {"content": system_config}


@router.post("/types/systemConfig/action/update")
def update_system_config(
    request: Request, config: SystemConfigUpdate, current_user=Depends(get_current_user)
):
    """Update system configuration for testing.

    This endpoint allows toggling between success and failure modes for testing,
    as well as configuring other system behaviors.
    """
    # Update only the provided fields
    if config.eligibility_status is not None:
        if config.eligibility_status not in ["success", "failure", "auto"]:
            raise HTTPException(
                status_code=400,
                detail="eligibility_status must be one of: 'success', 'failure', 'auto'",
            )
        system_config["eligibility_status"] = config.eligibility_status

    if config.failure_codes is not None:
        system_config["failure_codes"] = config.failure_codes

    if config.auto_failure_threshold is not None:
        if not 0 <= config.auto_failure_threshold <= 1:
            raise HTTPException(
                status_code=400, detail="auto_failure_threshold must be between 0 and 1"
            )
        system_config["auto_failure_threshold"] = config.auto_failure_threshold

    return {"content": system_config}
