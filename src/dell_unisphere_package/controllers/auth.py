"""Authentication controllers for Dell Unisphere API.

This module handles authentication and session management.
"""

import uuid
from fastapi import Request, HTTPException

from ..models.storage import sessions, users


# Authentication middleware
def get_current_user(request: Request):
    # First check for HTTP Basic Authentication
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Basic "):
        # Extract username and password from Authorization header
        import base64

        try:
            auth_decoded = base64.b64decode(auth_header[6:]).decode("utf-8")
            username, password = auth_decoded.split(":", 1)

            # Validate credentials
            if username in users and users[username]["password"] == password:
                # Create or update session
                session_id = str(uuid.uuid4())
                sessions[session_id] = {
                    "username": username,
                    "user_id": users[username]["id"],
                    "roles": users[username]["roles"],
                    "domain": users[username]["domain"],
                }

                # Return user info
                return sessions[session_id]
        except Exception:
            # If any error occurs during basic auth parsing, continue to cookie check
            pass

    # Then check for cookie-based authentication
    session_id = request.cookies.get("EMC-CSRF-TOKEN")
    if session_id and session_id in sessions:
        return sessions[session_id]

    # If no valid authentication found
    raise HTTPException(status_code=401, detail="Not authenticated")


# Helper function to format API response
def format_response(
    data, request: Request, base_url="/api", instance_type=None, instance_id=None
):
    """Format the API response according to Dell Unisphere API standards."""
    if isinstance(data, list):
        # Collection response
        entries = []
        for i, item in enumerate(data):
            entry = {"content": item}
            if instance_type:
                entry["id"] = f"{instance_type}_{i}"
            entries.append(entry)

        response = {
            "entries": entries,
        }

        # Add base URL
        base = f"{request.url.scheme}://{request.url.netloc}{base_url}"
        response["base"] = base

        return response
    else:
        # Single instance response
        if instance_id:
            return {"content": data, "id": instance_id}
        return data


# TODO: implement correct error codes as per API definition
def error_response(status_code: int, message: str):
    """Generate an error response in the format expected by Dell Unisphere API clients."""
    error_codes = {
        400: "0x6000",  # Bad request
        401: "0x6001",  # Unauthorized
        403: "0x6002",  # Forbidden
        404: "0x6003",  # Not found
        500: "0x6004",  # Internal server error
    }
    error_code = error_codes.get(status_code, "0x6000")
    return {
        "errorCode": error_code,
        "httpStatusCode": status_code,
        "messages": [{"en-US": message}],
    }
