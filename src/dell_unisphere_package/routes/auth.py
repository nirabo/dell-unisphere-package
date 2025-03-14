"""Authentication routes for Dell Unisphere API.

This module defines the API endpoints for authentication and user management.
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, Response

from ..controllers.auth import format_response, get_current_user
from ..models.storage import sessions, users
from ..schemas.base import LoginSessionInfo, User

router = APIRouter(prefix="/api")


@router.get("/types/loginSessionInfo/instances")
def get_login_session_info(
    request: Request, response: Response, current_user=Depends(get_current_user)
):
    """Get login session information or create a new session."""
    # At this point, current_user is already authenticated by the get_current_user dependency
    # We just need to ensure the CSRF token is set in both cookie and header

    # Get or create a session ID
    session_id = request.cookies.get("EMC-CSRF-TOKEN")
    if not session_id or session_id not in sessions:
        # If no valid session cookie exists, create a new one
        # This should rarely happen since get_current_user would have created a session
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            "username": current_user["username"],
            "user_id": current_user["user_id"],
            "roles": current_user["roles"],
            "domain": current_user["domain"],
        }

    # Set cookie and header
    response.set_cookie(
        key="EMC-CSRF-TOKEN",
        value=session_id,
        httponly=True,
        samesite="strict",
    )
    response.headers["EMC-CSRF-TOKEN"] = session_id

    # Create login session info
    login_session_info = LoginSessionInfo(
        domain=current_user["domain"].lower(),
        roles=current_user["roles"],
        user=User(id=f"user_{current_user['username']}"),
        id=session_id,
    )

    # Return formatted response
    return format_response(
        login_session_info,
        request,
        instance_type="loginSessionInfo",
        instance_id=session_id,
    )


@router.get("/types/user/instances")
def get_users(request: Request, current_user=Depends(get_current_user)):
    """Get list of users."""
    user_list = [{"id": user_info["id"]} for user_info in users.values()]
    return format_response(user_list, request, instance_type="user")


@router.delete("/types/loginSessionInfo/instances/{session_id}")
def logout_delete(
    session_id: str,
    request: Request,
    response: Response,
    current_user=Depends(get_current_user),
):
    """Logout and invalidate the session (DELETE method)."""
    cookie_session_id = request.cookies.get("EMC-CSRF-TOKEN")

    # Validate that the session ID in the URL matches the cookie
    if session_id != cookie_session_id:
        raise HTTPException(status_code=400, detail="Invalid session ID")

    # Remove session
    if cookie_session_id in sessions:
        del sessions[cookie_session_id]

    # Clear cookie
    response.delete_cookie(key="EMC-CSRF-TOKEN")

    # Create response message
    logout_message = {"message": "Logged out successfully"}

    # Return formatted response
    return format_response(logout_message, request, instance_type="logoutInfo")


@router.post("/types/loginSessionInfo/action/logout")
def logout_post(
    request: Request, response: Response, current_user=Depends(get_current_user)
):
    """Logout and invalidate the session (POST method)."""
    cookie_session_id = request.cookies.get("EMC-CSRF-TOKEN")

    # Remove session if it exists
    if cookie_session_id and cookie_session_id in sessions:
        del sessions[cookie_session_id]

    # Clear cookie
    response.delete_cookie(key="EMC-CSRF-TOKEN")

    # Create response message
    logout_message = {"message": "Logged out successfully"}

    # Return formatted response
    return format_response(logout_message, request, instance_type="logoutInfo")
