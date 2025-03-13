"""Software routes for Dell Unisphere API.

This module defines the API endpoints for installed software information.
"""

from fastapi import APIRouter, Request, Depends, HTTPException

from ..controllers.auth import get_current_user, format_response
from ..schemas.base import InstalledSoftwareVersion
from ..models.storage import installed_software_versions

router = APIRouter(prefix="/api")


@router.get("/types/installedSoftwareVersion/instances")
def get_installed_software_versions(
    request: Request, current_user=Depends(get_current_user)
):
    """Get all installed software versions."""
    versions = [
        InstalledSoftwareVersion(**version)
        for version in installed_software_versions.values()
    ]
    return format_response(versions, request, instance_type="installedSoftwareVersion")


@router.get("/instances/installedSoftwareVersion/{id}")
def get_installed_software_version(
    id: str, request: Request, current_user=Depends(get_current_user)
):
    """Get a specific installed software version by ID."""
    if id not in installed_software_versions:
        raise HTTPException(
            status_code=404, detail="Installed software version not found"
        )

    version = InstalledSoftwareVersion(**installed_software_versions[id])
    return format_response(
        version, request, instance_type="installedSoftwareVersion", instance_id=id
    )
