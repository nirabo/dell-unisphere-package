"""Headers verification middleware for Dell Unisphere API.

This module provides middleware to verify required headers for API requests.
"""

import logging
from typing import Callable, Dict, List

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

# Set up logger
logger = logging.getLogger(__name__)


class RequiredHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware that verifies required headers for API requests.

    This middleware checks for the presence of required headers for API requests,
    such as the X-EMC-REST-CLIENT header.
    """

    def __init__(
        self,
        app: ASGIApp,
        required_headers: Dict[str, str] = None,
        protected_paths: List[str] = None,
    ):
        """Initialize the middleware.

        Args:
            app: The ASGI application
            required_headers: Dictionary of required headers and their values
            protected_paths: List of path prefixes that require the headers
        """
        super().__init__(app)
        self.required_headers = required_headers or {"X-EMC-REST-CLIENT": "true"}
        self.protected_paths = protected_paths or ["/api", "/upload"]
        logger.info("Initialized RequiredHeadersMiddleware")

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request and verify required headers if needed.

        Args:
            request: The incoming request
            call_next: The next middleware or route handler

        Returns:
            The response from the next middleware or route handler
        """
        # Check if the request path is protected
        is_protected = any(
            request.url.path.startswith(path) for path in self.protected_paths
        )

        if is_protected:
            # Check for required headers
            for header_name, header_value in self.required_headers.items():
                if (
                    header_name not in request.headers
                    or request.headers[header_name] != header_value
                ):
                    logger.warning(
                        f"Missing or invalid required header {header_name} for request to {request.url.path}"
                    )
                    return JSONResponse(
                        status_code=401,
                        content={
                            "error": f"Missing or invalid required header: {header_name}"
                        },
                    )

        # If we get here, either the request doesn't need header verification or it has all required headers
        return await call_next(request)
