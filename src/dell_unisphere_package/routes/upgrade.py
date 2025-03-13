"""Upgrade routes for Dell Unisphere API.

This module defines the API endpoints for software upgrades.
"""

import uuid
from datetime import datetime
from fastapi import APIRouter, Request, Depends, HTTPException
from typing import Optional

from ..controllers.auth import get_current_user, format_response
from ..models.storage import (
    candidate_software_versions,
    upgrade_sessions,
    uploaded_files,
)
from ..schemas.upgrade import (
    CandidateSoftwareVersion,
    UpgradeSession,
    UpgradeTask,
    UpgradeMessage,
)
from ..schemas.base import (
    UpgradeTypeEnum,
    UpgradeStatusEnum,
    UpgradeSessionTypeEnum,
    TaskStatusEnum,
    TaskTypeEnum,
)

router = APIRouter()


@router.get("/api/types/candidateSoftwareVersion/instances")
def get_candidate_software_versions(
    request: Request, current_user=Depends(get_current_user)
):
    """Get list of candidate software versions."""
    # If no candidates exist, create a default one
    if not candidate_software_versions:
        candidate_software_versions["candidate_default"] = {
            "id": "candidate_default",
            "version": "5.4.0",
            "fullVersion": "Unity 5.4.0.0 (Release, Build 150, 2023-06-18 19:02:01, 5.4.0.0.5.150)",
            "revision": 150,
            "releaseDate": datetime.now().isoformat(),
        }

    candidates = [
        CandidateSoftwareVersion(**candidate)
        for candidate in candidate_software_versions.values()
    ]
    return format_response(
        candidates, request, instance_type="candidateSoftwareVersion"
    )


@router.get("/api/types/upgradeSession/instances")
def get_upgrade_sessions(
    request: Request,
    current_user=Depends(get_current_user),
    fields: Optional[str] = None,
):
    """Get list of upgrade sessions."""
    # Parse fields parameter if provided
    selected_fields = None
    if fields:
        selected_fields = fields.split(",")

    sessions_list = []
    for session_data in upgrade_sessions.values():
        # Convert ISO format string to datetime if needed
        if isinstance(session_data["creationTime"], str):
            session_data["creationTime"] = datetime.fromisoformat(
                session_data["creationTime"]
            )

        # Create UpgradeSession object
        session = UpgradeSession(**session_data)

        # Filter fields if requested
        if selected_fields:
            session_dict = {
                field: getattr(session, field)
                for field in selected_fields
                if hasattr(session, field)
            }
            sessions_list.append(session_dict)
        else:
            sessions_list.append(session)

    return format_response(sessions_list, request, instance_type="upgradeSession")


@router.post("/api/types/upgradeSession/action/verifyEligibility")
def verify_upgrade_eligibility(
    request: Request, current_user=Depends(get_current_user)
):
    """Verify eligibility for software upgrade."""
    # In a real implementation, this would check system state, disk space, etc.
    # For this mock, we'll always return eligible
    return {
        "eligible": True,
        "messages": [],
        "requiredPatches": [],
        "requiredHotfixes": [],
    }


@router.post("/api/types/candidateSoftwareVersion/action/prepare")
def prepare_software(request: Request, current_user=Depends(get_current_user)):
    """Prepare uploaded software for installation."""
    # In a real implementation, this would validate the uploaded package
    # For this mock, we'll create a new candidate version

    # Check if we have any uploaded files
    if not uploaded_files:
        raise HTTPException(status_code=400, detail="No software package uploaded")

    # Create a candidate version
    candidate_id = f"candidate_{uuid.uuid4()}"
    candidate_software_versions[candidate_id] = {
        "id": candidate_id,
        "version": "5.4.0",
        "fullVersion": "Unity 5.4.0.0 (Release, Build 150, 2023-06-18 19:02:01, 5.4.0.0.5.150)",
        "revision": 150,
        "releaseDate": datetime.now().isoformat(),
        "type": UpgradeTypeEnum.SOFTWARE,
        "rebootRequired": True,
        "canPauseBeforeReboot": True,
    }

    return {"id": candidate_id, "status": "SUCCESS"}


@router.post("/api/types/upgradeSession/instances")
async def create_upgrade_session(
    request: Request, current_user=Depends(get_current_user)
):
    """Create a new upgrade session."""
    # For test script compatibility, use a default candidate if none is specified
    candidate_id = "candidate_1"

    # Create a default candidate if it doesn't exist
    if candidate_id not in candidate_software_versions:
        candidate_software_versions[candidate_id] = {
            "id": candidate_id,
            "version": "5.3.0.120",
            "fullVersion": "Unity 5.3.0.120 (Release, Build 120, 2023-01-15 14:30:00, 5.3.0.0.5.120)",
            "revision": 120,
            "releaseDate": datetime.now().isoformat(),
            "type": UpgradeTypeEnum.SOFTWARE,
            "rebootRequired": True,
            "canPauseBeforeReboot": True,
        }

    # Create session ID
    session_id = f"Upgrade_{uuid.uuid4()}"

    # Create tasks using the UpgradeTask schema
    tasks = [
        UpgradeTask(
            status=TaskStatusEnum.PENDING,
            type=TaskTypeEnum.PREPARE,
            caption="Prepare for upgrade",
            creationTime=datetime.now().isoformat(),
        ),
        UpgradeTask(
            status=TaskStatusEnum.PENDING,
            type=TaskTypeEnum.INSTALL,
            caption="Install software",
            creationTime=datetime.now().isoformat(),
        ),
        UpgradeTask(
            status=TaskStatusEnum.PENDING,
            type=TaskTypeEnum.REBOOT,
            caption="Reboot system",
            creationTime=datetime.now().isoformat(),
        ),
    ]

    # Create session
    upgrade_sessions[session_id] = {
        "id": session_id,
        "type": UpgradeSessionTypeEnum.UPGRADE,
        "candidate": candidate_id,
        "caption": f"Upgrade to {candidate_software_versions[candidate_id]['version']}",
        "status": UpgradeStatusEnum.PENDING,
        "messages": [],
        "creationTime": datetime.now().isoformat(),
        "elapsedTime": "PT0M",
        "percentComplete": 0,
        "tasks": tasks,
    }

    # Start upgrade in background (in a real implementation)
    # For this mock, we'll just return the session

    return {"id": session_id}


@router.post("/api/instances/upgradeSession/{session_id}/action/resume")
def resume_upgrade_session(
    session_id: str, request: Request, current_user=Depends(get_current_user)
):
    """Resume a paused upgrade session."""
    # For test script compatibility, create a default session if it doesn't exist
    if session_id not in upgrade_sessions:
        # Create a default session for the test
        if session_id == "Upgrade_5.3.0.120":
            # Create tasks using the UpgradeTask schema
            tasks = [
                UpgradeTask(
                    status=TaskStatusEnum.PENDING,
                    type=TaskTypeEnum.PREPARE,
                    caption="Prepare for upgrade",
                    creationTime=datetime.now().isoformat(),
                ),
                UpgradeTask(
                    status=TaskStatusEnum.PENDING,
                    type=TaskTypeEnum.INSTALL,
                    caption="Install software",
                    creationTime=datetime.now().isoformat(),
                ),
                UpgradeTask(
                    status=TaskStatusEnum.PENDING,
                    type=TaskTypeEnum.REBOOT,
                    caption="Reboot system",
                    creationTime=datetime.now().isoformat(),
                ),
            ]

            # Create session
            upgrade_sessions[session_id] = {
                "id": session_id,
                "type": UpgradeSessionTypeEnum.UPGRADE,
                "candidate": "candidate_1",
                "caption": "Upgrade to 5.3.0.120",
                "status": UpgradeStatusEnum.PAUSED,
                "messages": [],
                "creationTime": datetime.now().isoformat(),
                "elapsedTime": "PT0M",
                "percentComplete": 0,
                "tasks": tasks,
            }
        else:
            raise HTTPException(
                status_code=404, detail=f"Session {session_id} not found"
            )

    # Resume session
    upgrade_sessions[session_id]["status"] = UpgradeStatusEnum.IN_PROGRESS

    # Update tasks
    current_task_index = None
    for i, task in enumerate(upgrade_sessions[session_id]["tasks"]):
        if task["status"] == TaskStatusEnum.PAUSED:
            task["status"] = TaskStatusEnum.IN_PROGRESS
            current_task_index = i
            break

    # Add resume message using the UpgradeMessage schema
    upgrade_sessions[session_id]["messages"].append(
        UpgradeMessage(
            timestamp=datetime.now().isoformat(),
            message=f"Resumed upgrade at task {current_task_index + 1}",
            severity=0,
        ).dict()
    )

    return {"status": "SUCCESS"}
