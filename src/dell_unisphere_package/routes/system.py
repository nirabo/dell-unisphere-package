"""System routes for Dell Unisphere API.

This module defines the API endpoints for system information and upgrades.
"""

from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Request

from ..controllers.auth import format_response
from ..models.storage import (
    get_system_info,
    get_version_history,
    update_software_version,
)
from ..schemas.base import BasicSystemInfo

router = APIRouter(prefix="/api")


@router.get("/types/basicSystemInfo/instances")
def get_basic_system_info(request: Request) -> Dict[str, Any]:
    """Get basic system information."""
    try:
        # Get system info from the database
        db_system_info = get_system_info()

        # Create a BasicSystemInfo object from the database data
        system_info = BasicSystemInfo(
            id=db_system_info.get("id", "0"),
            model=db_system_info.get("model", "Unity 380F"),
            name=db_system_info.get("name", "CKM01204905476"),
            softwareVersion=db_system_info.get("softwareVersion", "5.3.0"),
            softwareFullVersion=db_system_info.get(
                "softwareFullVersion",
                "Unity 5.3.0.0 (Release, Build 120, 2023-03-18 19:02:01, 5.3.0.0.5.120)",
            ),
            apiVersion=db_system_info.get("apiVersion", "13.0"),
            earliestApiVersion=db_system_info.get("earliestApiVersion", "4.0"),
        )

        return format_response([system_info], request, instance_type="basicSystemInfo")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/types/versionHistory/instances")
def get_version_history_info(request: Request) -> Dict[str, Any]:
    """Get version history information."""
    try:
        # Get version history from the database
        version_history = get_version_history()
        return format_response(version_history, request, instance_type="versionHistory")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/types/upgradeSession/instances")
def create_upgrade_session(request: Request, data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new upgrade session."""
    try:
        candidate_version = data.get("candidate")
        if not candidate_version:
            raise HTTPException(status_code=400, detail="Candidate version is required")

        # Create a new upgrade session
        session_id = "upgrade_session_1"  # TODO: Implement proper session ID generation
        return {"id": session_id, "status": "PENDING", "candidate": candidate_version}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/types/upgradeSession/action/verifyUpgradeEligibility")
def verify_upgrade_eligibility(
    request: Request, data: Dict[str, Any]
) -> Dict[str, Any]:
    """Verify if the system is eligible for upgrade."""
    try:
        candidate_version = data.get("candidate")
        if not candidate_version:
            raise HTTPException(status_code=400, detail="Candidate version is required")

        # Verify upgrade eligibility
        return format_response(
            [
                {
                    "eligible": True,
                    "candidate": candidate_version,
                    "current": get_system_info().get("softwareVersion", "5.3.0"),
                }
            ],
            request,
            instance_type="upgradeSession",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/types/candidateSoftwareVersion/action/prepare")
def prepare_software_version(request: Request, data: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare a software version for upgrade."""
    try:
        filename = data.get("filename")
        if not filename:
            raise HTTPException(status_code=400, detail="Filename is required")

        # Prepare the software version
        return format_response(
            [{"status": "PREPARED", "filename": filename}],
            request,
            instance_type="candidateSoftwareVersion",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/types/upgradeSession/action/completeUpgrade")
def complete_upgrade(request: Request, data: Dict[str, Any]) -> Dict[str, Any]:
    """Complete the upgrade process."""
    try:
        session_id = data.get("session_id")
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required")

        # Update system version
        new_version = "5.4.0"  # TODO: Get actual version from candidate
        update_software_version(new_version, 130)

        return format_response(
            [
                {
                    "status": "COMPLETED",
                    "session_id": session_id,
                    "new_version": new_version,
                }
            ],
            request,
            instance_type="upgradeSession",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
