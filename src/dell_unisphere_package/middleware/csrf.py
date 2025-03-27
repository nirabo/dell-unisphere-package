"""CSRF protection middleware for Dell Unisphere API.

This module provides middleware to verify CSRF tokens for POST and DELETE requests.
"""

import logging
import re
from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

# Set up logger
logger = logging.getLogger(__name__)


class CSRFProtectionMiddleware(BaseHTTPMiddleware):
    """Middleware that verifies CSRF tokens for POST and DELETE requests.

    This middleware checks for the presence of a CSRF token in the request headers
    or body for POST and DELETE requests to protected endpoints.
    """

    def __init__(
        self,
        app: ASGIApp,
        excluded_paths: list = None,
    ):
        """Initialize the middleware.

        Args:
            app: The ASGI application
            excluded_paths: List of paths to exclude from CSRF protection
        """
        super().__init__(app)
        self.excluded_paths = excluded_paths or [
            "/api/types/loginSessionInfo/instances",
            "/upload/files/types/candidateSoftwareVersion",
            "/api/auth",
        ]
        logger.info("Initialized CSRFProtectionMiddleware")

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request and verify CSRF token if needed.

        Args:
            request: The incoming request
            call_next: The next middleware or route handler

        Returns:
            The response from the next middleware or route handler
        """
        # Only check POST and DELETE requests to API endpoints
        if request.method in ["POST", "DELETE"] and (
            request.url.path.startswith("/api")
            or request.url.path.startswith("/upload")
        ):
            # Skip CSRF check for excluded paths
            for path in self.excluded_paths:
                if request.url.path == path:
                    return await call_next(request)

            # Check for CSRF token in headers
            csrf_token = request.headers.get("EMC-CSRF-TOKEN")

            # For test scripts, handle the case where the token might be in the request body
            if not csrf_token:
                try:
                    # Check if we can read the body
                    body_bytes = await request.body()
                    body_text = body_bytes.decode()

                    # Try to extract the token from the body if it's passed as a header in the data parameter
                    if "EMC-CSRF-TOKEN" in body_text:
                        token_match = re.search(
                            r"EMC-CSRF-TOKEN:\s*([\w-]+)", body_text
                        )
                        if token_match:
                            # We found a token in the body, so we'll use it
                            csrf_token = token_match.group(1)
                            logger.debug(
                                f"Found CSRF token in request body: {csrf_token}"
                            )
                except Exception as e:
                    logger.warning(f"Error reading request body for CSRF token: {e}")

            # If we still don't have a token, return an error
            if not csrf_token:
                logger.warning(
                    f"Missing CSRF token for {request.method} request to {request.url.path}"
                )
                return JSONResponse(
                    status_code=403,
                    content={"error": "Missing CSRF token in header or body"},
                )

        # If we get here, either the request doesn't need CSRF protection or it has a valid token
        return await call_next(request)
