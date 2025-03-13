"""Test API server for Dell Unisphere Mock API.

This module provides a standalone FastAPI server that implements the basic endpoints
needed to test the Dell Unisphere API interactions.
"""

from fastapi import FastAPI, Depends, HTTPException, Request, Response, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime, timedelta
from enum import Enum
import uuid
import secrets
from pydantic import BaseModel

FullVersion = "Unity 5.3.0.0 (Release, Build 120, 2023-03-18 19:02:01, 5.3.0.0.5.120)"

# Create FastAPI application
app = FastAPI(
    title="Dell EMC Unisphere Test API",
    description="A test implementation of the Dell EMC Unisphere REST API",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
sessions = {}
users = {
    "admin": {
        "id": "user_admin",
        "password": "Password123!",
        "roles": [{"id": "administrator"}],
        "domain": "local",
    },
    "user": {
        "id": "user_user",
        "password": "Password123!",
        "roles": [{"id": "user"}],
        "domain": "local",
    },
    "diagnose": {
        "id": "user_diagnose",
        "password": "Password123!",
        "roles": [{"id": "diagnose"}],
        "domain": "local",
    },
}
candidate_software_versions = {}
upgrade_sessions = {
    "Upgrade_4.3.0.1499782821": {
        "id": "Upgrade_4.3.0.1499782821",
        "type": 0,  # UPGRADE
        "candidate": "candidate_default",
        "caption": "Upgrade_4.3.0.1499782821",
        "status": 2,  # COMPLETED
        "messages": [],
        "creationTime": (datetime.now() - timedelta(days=30)).isoformat(),
        "elapsedTime": "PT2H30M",
        "percentComplete": 100,
        "tasks": [],
    }
}
uploaded_files = {}


# Models
class BasicSystemInfo(BaseModel):
    id: str = "0"
    model: str = "Unity 380F"
    name: str = "CKM01204905476"
    softwareVersion: str = "5.3.0"
    softwareFullVersion: str = (
        "Unity 5.3.0.0 (Release, Build 120, 2023-03-18 19:02:01, 5.3.0.0.5.120)"
    )
    apiVersion: str = "13.0"
    earliestApiVersion: str = "4.0"


class User(BaseModel):
    id: str


class Role(BaseModel):
    id: str


class LoginSessionInfo(BaseModel):
    roles: List[Role]
    domain: str
    user: User
    id: str
    idleTimeout: int = 3600
    isPasswordChangeRequired: bool = False


class UpgradeTypeEnum(str, Enum):
    SOFTWARE = "SOFTWARE"
    LANGUAGE_PACK = "LANGUAGE_PACK"


class UpgradeStatusEnum(int, Enum):
    PENDING = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    FAILED = 3
    PAUSED = 4


class UpgradeSessionTypeEnum(int, Enum):
    UPGRADE = 0
    INSTALL = 1


class TaskStatusEnum(int, Enum):
    PENDING = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    FAILED = 3
    PAUSED = 4


class TaskTypeEnum(int, Enum):
    PREPARE = 0
    UPLOAD = 1
    INSTALL = 2
    REBOOT = 3


class CandidateSoftwareVersion(BaseModel):
    id: str
    version: str
    fullVersion: str
    revision: int
    releaseDate: datetime
    type: UpgradeTypeEnum = UpgradeTypeEnum.SOFTWARE
    rebootRequired: bool = True
    canPauseBeforeReboot: bool = True


class UpgradeTask(BaseModel):
    status: TaskStatusEnum
    type: TaskTypeEnum
    caption: str
    creationTime: datetime
    estRemainTime: str = "00:03:30.000"


class UpgradeMessage(BaseModel):
    timestamp: datetime
    message: str
    severity: int = 0


class UpgradeSession(BaseModel):
    id: str
    type: UpgradeSessionTypeEnum = UpgradeSessionTypeEnum.UPGRADE
    candidate: str  # Reference to CandidateSoftwareVersion id
    caption: str
    status: UpgradeStatusEnum
    messages: List[UpgradeMessage] = []
    creationTime: datetime
    elapsedTime: timedelta = timedelta(minutes=0)
    percentComplete: int = 0
    tasks: List[UpgradeTask] = []


# Middleware to check for required headers
async def verify_required_headers(request: Request, call_next):
    # Check for X-EMC-REST-CLIENT header
    if request.url.path.startswith("/api") or request.url.path.startswith("/upload"):
        if (
            "X-EMC-REST-CLIENT" not in request.headers
            or request.headers["X-EMC-REST-CLIENT"] != "true"
        ):
            return JSONResponse(
                status_code=401,
                content={"error": "Missing or invalid X-EMC-REST-CLIENT header"},
            )

    response = await call_next(request)
    return response


# Add middleware to check for required headers
app.middleware("http")(verify_required_headers)


# Authentication middleware
def get_current_user(request: Request):
    session_id = request.cookies.get("EMC-CSRF-TOKEN")
    if session_id and session_id in sessions:
        return sessions[session_id]

    # For basic auth, check Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Basic "):
        import base64

        credentials = base64.b64decode(auth_header[6:]).decode("utf-8")
        username, password = credentials.split(":", 1)
        if username in users and users[username]["password"] == password:
            return users[username]

    return None


# Helper function to format API response
def format_response(
    data, request: Request, base_url="/api", instance_type=None, instance_id=None
):
    now = datetime.now().isoformat() + "Z"
    host = f"{request.url.scheme}://{request.url.hostname}:{request.url.port}"

    if isinstance(data, list):
        entries = []
        for item in data:
            if isinstance(item, dict) and "id" in item:
                item_id = item["id"]
                entries.append(
                    {
                        "@base": f"{host}{base_url}/instances/{instance_type}",
                        "updated": now,
                        "links": [{"rel": "self", "href": f"/{item_id}"}],
                        "content": {"id": item_id},
                    }
                )
            else:
                entries.append(item)

        return {
            "@base": f"{host}{base_url}/types/{instance_type}/instances?per_page=2000",
            "updated": now,
            "links": [{"rel": "self", "href": "&page=1"}],
            "entries": entries,
        }
    elif isinstance(data, dict):
        return {
            "@base": f"{host}{base_url}/instances/{instance_type}",
            "updated": now,
            "links": [{"rel": "self", "href": f"/{instance_id}"}],
            "content": data,
        }
    else:
        return data


# Error response
def error_response(status_code: int, message: str):
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "errorCode": 131149829,
                "httpStatusCode": status_code,
                "messages": [{"en-US": message}],
                "created": datetime.now().isoformat() + "Z",
            }
        },
    )


# Routes
@app.get("/api/types/basicSystemInfo/instances")
async def get_basic_system_info(request: Request):
    system_info = BasicSystemInfo()
    return format_response(
        [system_info.dict()], request, instance_type="basicSystemInfo"
    )


@app.get("/api/types/loginSessionInfo/instances")
async def get_login_session_info(
    request: Request, response: Response, current_user=Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Generate CSRF token
    csrf_token = secrets.token_urlsafe(32)
    sessions[csrf_token] = current_user

    # Set cookie and CSRF token in header as per Authentication.md
    response.set_cookie(
        key="EMC-CSRF-TOKEN",
        value=csrf_token,
        httponly=True,
        samesite="lax",
        max_age=3600,
    )

    # Also set header for CSRF token as per Authentication.md
    response.headers["EMC-CSRF-TOKEN"] = csrf_token

    # Return the login session info
    session_info = LoginSessionInfo(
        roles=[Role(id=role["id"]) for role in current_user["roles"]],
        domain=current_user["domain"],
        user=User(id=current_user["id"]),
        id="user",
    )

    return format_response(
        [session_info.dict()], request, instance_type="loginSessionInfo"
    )


# Authentication is handled implicitly through the loginSessionInfo endpoint
# as per the official documentation in Authentication.md
# The CSRF token is returned in the response headers of GET requests


@app.get("/api/types/user/instances")
async def get_users(request: Request, current_user=Depends(get_current_user)):
    if not current_user:
        return error_response(401, "Unauthorized")

    user_list = [{"id": user["id"]} for user in users.values()]
    return format_response(user_list, request, instance_type="user")


@app.get("/api/types/candidateSoftwareVersion/instances")
async def get_candidate_software_versions(
    request: Request, current_user=Depends(get_current_user)
):
    if not current_user:
        return error_response(401, "Unauthorized")

    candidates = list(candidate_software_versions.values())
    return format_response(
        candidates, request, instance_type="candidateSoftwareVersion"
    )


@app.get("/api/types/upgradeSession/instances")
async def get_upgrade_sessions(
    request: Request,
    current_user=Depends(get_current_user),
    fields: Optional[str] = None,
):
    if not current_user:
        return error_response(401, "Unauthorized")

    sessions_list = []
    if fields:
        field_list = fields.split(",")
        for session in upgrade_sessions.values():
            filtered_session = {
                field: session.get(field) for field in field_list if field in session
            }
            filtered_session["id"] = session["id"]
            sessions_list.append(filtered_session)
    else:
        sessions_list = list(upgrade_sessions.values())

    return format_response(sessions_list, request, instance_type="upgradeSession")


@app.post("/api/types/upgradeSession/action/verifyUpgradeEligibility")
async def verify_upgrade_eligibility(
    request: Request, current_user=Depends(get_current_user)
):
    if not current_user:
        return error_response(401, "Unauthorized")

    # Check CSRF token
    csrf_token = request.headers.get("EMC-CSRF-TOKEN")
    if not csrf_token or csrf_token not in sessions:
        return error_response(403, "Invalid CSRF token")

    # Simulate eligibility verification
    return {"isEligible": True, "messages": []}


@app.post("/upload/files/types/candidateSoftwareVersion")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    if not current_user:
        return error_response(401, "Unauthorized")

    # Check CSRF token
    csrf_token = request.headers.get("EMC-CSRF-TOKEN")
    if not csrf_token or csrf_token not in sessions:
        return error_response(403, "Invalid CSRF token")

    # Save file info (not the actual file in this mock)
    file_id = f"file_{uuid.uuid4()}"
    uploaded_files[file_id] = {
        "id": file_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "size": 0,  # We're not actually saving the file
        "upload_time": datetime.now(),
    }

    return {"id": file_id, "filename": file.filename, "status": "UPLOADED"}


@app.post("/api/types/candidateSoftwareVersion/action/prepare")
async def prepare_software(request: Request, current_user=Depends(get_current_user)):
    if not current_user:
        return error_response(401, "Unauthorized")

    # Check CSRF token
    csrf_token = request.headers.get("EMC-CSRF-TOKEN")
    if not csrf_token or csrf_token not in sessions:
        return error_response(403, "Invalid CSRF token")

    # Get request body
    body = await request.json()
    filename = body.get("filename")

    if not filename:
        return error_response(400, "Filename is required")

    # Create a candidate software version
    candidate_id = f"candidate_{uuid.uuid4().hex[:8]}"
    candidate = {
        "id": candidate_id,
        "version": "5.3.0",
        "fullVersion": FullVersion,
        "revision": 120,
        "releaseDate": datetime.now().isoformat(),
        "type": "SOFTWARE",
        "rebootRequired": True,
        "canPauseBeforeReboot": True,
    }

    candidate_software_versions[candidate_id] = candidate

    return {"id": candidate_id, "status": "PREPARED"}


@app.post("/api/types/upgradeSession/instances")
async def create_upgrade_session(
    request: Request, current_user=Depends(get_current_user)
):
    if not current_user:
        return error_response(401, "Unauthorized")

    # Check CSRF token
    csrf_token = request.headers.get("EMC-CSRF-TOKEN")
    if not csrf_token or csrf_token not in sessions:
        return error_response(403, "Invalid CSRF token")

    # Get request body
    body = await request.json()
    candidate_id = body.get("candidate")
    pause_before_reboot = body.get("pauseBeforeReboot", False)

    if not candidate_id:
        return error_response(400, "Candidate ID is required")

    if (
        candidate_id not in candidate_software_versions
        and candidate_id != "candidate_1"
    ):
        return error_response(404, "Candidate not found")

    # Create an upgrade session
    session_id = f"Upgrade_5.3.0.{uuid.uuid4().hex[:8]}"
    now = datetime.now()

    session = {
        "id": session_id,
        "type": 0,  # UPGRADE
        "candidate": candidate_id,
        "caption": session_id,
        "status": 0,  # PENDING
        "messages": [
            {
                "timestamp": now.isoformat(),
                "message": "Upgrade session created",
                "severity": 0,
            }
        ],
        "creationTime": now.isoformat(),
        "elapsedTime": "PT0S",
        "percentComplete": 0,
        "tasks": [
            {
                "status": 0,  # PENDING
                "type": 0,  # PREPARE
                "caption": "Preparing system",
                "creationTime": now.isoformat(),
                "estRemainTime": "00:03:30.000",
            }
        ],
        "pauseBeforeReboot": pause_before_reboot,
    }

    upgrade_sessions[session_id] = session

    return {"id": session_id, "status": "CREATED"}


@app.post("/api/instances/upgradeSession/{session_id}/action/resume")
async def resume_upgrade_session(
    session_id: str, request: Request, current_user=Depends(get_current_user)
):
    if not current_user:
        return error_response(401, "Unauthorized")

    # Check CSRF token
    csrf_token = request.headers.get("EMC-CSRF-TOKEN")
    if not csrf_token or csrf_token not in sessions:
        return error_response(403, "Invalid CSRF token")

    if session_id not in upgrade_sessions:
        return error_response(404, "Upgrade session not found")

    session = upgrade_sessions[session_id]

    # For testing purposes, allow resuming any session
    # if session["status"] not in [3, 4]:  # FAILED or PAUSED
    #     return error_response(400, "Session is not in a resumable state")

    # Update session status
    session["status"] = 1  # IN_PROGRESS
    now = datetime.now()
    session["messages"].append(
        {
            "timestamp": now.isoformat(),
            "message": "Upgrade session resumed",
            "severity": 0,
        }
    )

    # Update task status
    for task in session["tasks"]:
        if task["status"] in [0, 3, 4]:  # PENDING, FAILED or PAUSED
            task["status"] = 1  # IN_PROGRESS

    return {"id": session_id, "status": "RESUMED"}


@app.post("/api/types/loginSessionInfo/action/logout")
async def logout(
    request: Request, response: Response, current_user=Depends(get_current_user)
):
    if not current_user:
        return error_response(401, "Unauthorized")

    # Check CSRF token
    csrf_token = request.headers.get("EMC-CSRF-TOKEN")
    if csrf_token and csrf_token in sessions:
        del sessions[csrf_token]

    # Clear cookie
    response.delete_cookie(key="EMC-CSRF-TOKEN")

    return {"status": "LOGGED_OUT"}


# Run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
