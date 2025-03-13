"""Upload routes for Dell Unisphere API.

This module defines the API endpoints for file uploads, specifically for software upgrades.
"""

import uuid
from datetime import datetime
from fastapi import APIRouter, Request, Depends, File, UploadFile

from ..controllers.auth import get_current_user
from ..models.storage import uploaded_files

router = APIRouter()


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
    # Generate a unique ID for the file
    file_id = f"file_{uuid.uuid4()}"

    # Read file content (in a real implementation, would save to disk)
    content = await file.read()

    # Store file metadata
    uploaded_files[file_id] = {
        "id": file_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "upload_time": datetime.now().isoformat(),
        "type": "candidateSoftwareVersion",
    }

    return {"id": file_id, "filename": file.filename, "size": len(content)}
