"""Authentication controllers for Dell Unisphere API.

This module handles authentication and session management.
"""

import uuid

from fastapi import HTTPException, Request

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
    from datetime import datetime

    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    if isinstance(data, list):
        # Collection response
        base_url_path = f"{base_url}/types/{instance_type}/instances"
        full_base_url = (
            f"{request.url.scheme}://{request.url.netloc}{base_url_path}?per_page=2000"
        )

        entries = []
        for i, item in enumerate(data):
            item_id = getattr(item, "id", f"{i}")
            instance_base_url = f"{request.url.scheme}://{request.url.netloc}{base_url}/instances/{instance_type}"

            entry = {
                "@base": instance_base_url,
                "content": item,
                "links": [{"rel": "self", "href": f"/{item_id}"}],
                "updated": current_time,
            }
            entries.append(entry)

        response = {
            "@base": full_base_url,
            "updated": current_time,
            "links": [{"rel": "self", "href": "&page=1"}],
            "entries": entries,
        }

        return response
    else:
        # Single instance response
        instance_base_url = f"{request.url.scheme}://{request.url.netloc}{base_url}/instances/{instance_type}"
        if instance_id:
            response = {
                "@base": instance_base_url,
                "content": data,
                "links": [{"rel": "self", "href": f"/{instance_id}"}],
                "updated": current_time,
            }
            return response
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
