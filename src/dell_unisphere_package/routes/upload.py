"""Upload routes for Dell Unisphere API.

This module defines the API endpoints for file uploads, specifically for software upgrades.
Implements the single-candidate policy where only one upgrade candidate can exist at a time.
"""

import asyncio
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile

from ..controllers.auth import get_current_user
from ..models.storage import candidate_software_versions, uploaded_files

router = APIRouter()

# Lock for handling concurrent uploads
upload_lock = asyncio.Lock()


@router.post("/upload/files/types/candidateSoftwareVersion")
async def upload_candidate_software(
    request: Request,
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    """Upload a software package candidate.

    This endpoint allows uploading upgrade candidates (software or firmware) and language packs
    to the storage system to make them available to install.

    Note: When you upload an upgrade candidate file onto the storage system, it replaces
    the previous version. There can only be one upgrade candidate on the system at a time.
    """
    async with upload_lock:
        # Generate a unique ID for the file
        file_id = f"file_{uuid.uuid4()}"

        try:
            # Read file content (in a real implementation, would save to disk)
            content = await file.read()

            # Clear any existing candidates before storing the new one
            uploaded_files.clear()
            candidate_software_versions.clear()

            # Store file metadata
            uploaded_files[file_id] = {
                "id": file_id,
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(content),
                "upload_time": datetime.now().isoformat(),
                "type": "candidateSoftwareVersion",
            }

            # Create a candidate software version entry
            # In a real implementation, this would parse the file content
            # to extract version information
            candidate_software_versions[file_id] = {
                "id": file_id,
                "version": "5.4.0.0",  # Example version
                "fullVersion": f"Unity {file.filename}",
                "revision": 0,
                "releaseDate": datetime.now().isoformat(),
                "type": "SOFTWARE",
                "rebootRequired": True,
                "canPauseBeforeReboot": True,
            }

            return {"id": file_id, "filename": file.filename, "size": len(content)}

        except Exception as e:
            # If anything fails during upload, ensure we don't leave partial state
            uploaded_files.pop(file_id, None)
            candidate_software_versions.pop(file_id, None)
            raise HTTPException(status_code=500, detail=str(e))
