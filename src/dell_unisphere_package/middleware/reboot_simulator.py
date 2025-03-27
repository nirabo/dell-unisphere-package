"""Middleware for simulating connection resets during system reboot.

This module provides middleware to simulate connection resets that occur
during the system reboot phase of an upgrade process.
"""

import logging
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from ..models.storage import upgrade_sessions
from ..schemas.base import TaskStatusEnum

# Set up logger
logger = logging.getLogger(__name__)


class RebootSimulatorMiddleware(BaseHTTPMiddleware):
    """Middleware that simulates connection resets during system reboot.

    This middleware checks if any upgrade session has a task with the caption
    "Rebooting the primary SP" that is currently in progress. If such a task
    is found, the middleware will close the connection to simulate a real
    system reboot.
    """

    def __init__(
        self,
        app: ASGIApp,
        reboot_task_caption: str = "Rebooting the primary SP",
        reset_probability: float = 1.0,
    ):
        """Initialize the middleware.

        Args:
            app: The ASGI application
            reboot_task_caption: The caption of the task that triggers the connection reset
            reset_probability: Probability of resetting the connection (0.0 to 1.0)
        """
        super().__init__(app)
        self.reboot_task_caption = reboot_task_caption
        self.reset_probability = min(
            max(reset_probability, 0.0), 1.0
        )  # Ensure between 0 and 1
        self.excluded_paths = [
            "/docs",
            "/openapi.json",
            "/redoc",
            "/static",
        ]
        logger.info(
            f"Initialized RebootSimulatorMiddleware with reboot task caption: {reboot_task_caption}"
        )

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request and simulate connection resets if needed.

        Args:
            request: The incoming request
            call_next: The next middleware or route handler

        Returns:
            The response from the next middleware or route handler
        """
        # Skip middleware for excluded paths
        for path in self.excluded_paths:
            if request.url.path.startswith(path):
                return await call_next(request)

        # Check if any session has the reboot task in progress
        should_reset = self._check_for_reboot_task()

        if should_reset:
            # Log the connection reset
            client_host = request.client.host if request.client else "unknown"
            logger.info(
                f"Simulating connection reset for {client_host} during system reboot"
            )

            # Return a response that will cause a connection reset
            # This is done by returning a response with an invalid status code
            # that will cause the server to close the connection
            return Response(
                content="Connection reset by peer",
                status_code=444,  # Nginx's "Connection Closed Without Response" code
                headers={"Connection": "close"},
            )

        # If no reset is needed, proceed with the normal request
        return await call_next(request)

    def _check_for_reboot_task(self) -> bool:
        """Check if any upgrade session has the reboot task in progress.

        Returns:
            True if a reboot task is in progress, False otherwise
        """
        import random

        # First check if we should apply the probability filter
        if self.reset_probability < 1.0 and random.random() > self.reset_probability:
            return False

        # Check all active upgrade sessions
        for session_id, session in upgrade_sessions.items():
            # Skip sessions that don't have tasks
            if "tasks" not in session:
                continue

            # Check each task in the session
            for task in session["tasks"]:
                # Handle both dictionary and Pydantic model access
                if isinstance(task, dict):
                    task_caption = task.get("caption")
                    task_status = task.get("status")
                else:
                    # Access attributes directly for Pydantic models
                    task_caption = task.caption
                    task_status = task.status

                if (
                    task_caption == self.reboot_task_caption
                    and task_status == TaskStatusEnum.IN_PROGRESS
                ):
                    logger.info(
                        f"Found active reboot task in session {session_id}: {task_caption}"
                    )
                    return True

        return False
