"""Test API server for Dell Unisphere Mock API.

This module provides a standalone FastAPI server that implements the basic endpoints
needed to test the Dell Unisphere API interactions.
"""

import atexit
import logging
import logging.config

# Register signal handlers to save state on SIGINT and SIGTERM
import signal
import sys
import threading

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .middleware import (
    CSRFProtectionMiddleware,
    RebootSimulatorMiddleware,
    RequiredHeadersMiddleware,
)
from .routes import router

# Configure logging
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "fmt": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "dell_unisphere_package": {
            "level": "INFO",
            "handlers": ["default"],
            "propagate": False,
        },
    },
}

# Flag to prevent multiple signal handlers from running simultaneously
_shutdown_in_progress = threading.Event()

logging.config.dictConfig(logging_config)
logger = logging.getLogger("dell_unisphere_package")

# Store the original openapi function
original_openapi = FastAPI.openapi

# Module-level variable to store the OpenAPI schema
_openapi_schema = None


def custom_openapi():
    """Custom OpenAPI schema generator with authentication support."""
    global _openapi_schema

    if _openapi_schema:
        return _openapi_schema

    # Get the original schema
    openapi_schema = original_openapi(app)

    # Add security schemes
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    openapi_schema["components"]["securitySchemes"] = {
        "basicAuth": {
            "type": "http",
            "scheme": "basic",
            "description": "Basic authentication with username and password",
        },
        "emcRestClient": {
            "type": "apiKey",
            "in": "header",
            "name": "X-EMC-REST-CLIENT",
            "description": "Required header for all API requests",
        },
        "emcCsrfToken": {
            "type": "apiKey",
            "in": "header",
            "name": "EMC-CSRF-TOKEN",
            "description": "Required header for POST and DELETE requests. Obtained from login session info.",
        },
    }

    # Apply security schemes to all operations
    for path in openapi_schema["paths"].values():
        for method, operation in path.items():
            # Skip OPTIONS method
            if method.lower() == "options":
                continue

            if "security" not in operation:
                operation["security"] = [
                    {"basicAuth": []},
                    {"emcRestClient": []},
                ]
            # Add CSRF token requirement for POST and DELETE methods
            if method.lower() in ["post", "delete"]:
                operation["security"].append({"emcCsrfToken": []})

    _openapi_schema = openapi_schema
    return _openapi_schema


# Swagger UI parameters for handling authentication
SWAGGER_UI_PARAMETERS = {
    "persistAuthorization": True,
    "requestInterceptor": """
    (req) => {
        console.log('Starting request interceptor');

        // Add X-EMC-REST-CLIENT header to all requests
        req.headers['X-EMC-REST-CLIENT'] = 'true';

        // For POST and DELETE requests, add CSRF token if available
        if (['POST', 'DELETE'].includes(req.method.toUpperCase())) {
            // Get token from localStorage
            const storedToken = localStorage.getItem('emc_csrf_token');
            if (storedToken) {
                req.headers['EMC-CSRF-TOKEN'] = storedToken;
                console.log('Added stored CSRF token:', storedToken);
            } else {
                console.log('No CSRF token found in storage');
            }
        }

        console.log('Final request headers:', req.headers);
        return req;
    }""",
    "responseInterceptor": """
    (response) => {
        console.log('Response interceptor:', response.url);

        // Get CSRF token from response headers
        const token = response.headers.get('EMC-CSRF-TOKEN');
        if (token) {
            console.log('Got CSRF token from response:', token);
            localStorage.setItem('emc_csrf_token', token);
        }

        return response;
    }""",
}

# Create FastAPI application
app = FastAPI(
    title="Dell EMC Unisphere Test API",
    description="A test implementation of the Dell EMC Unisphere REST API",
    version="0.2.0",
    swagger_ui_parameters=SWAGGER_UI_PARAMETERS,
)

# Set custom OpenAPI schema
app.openapi = custom_openapi

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middleware in the correct order (from innermost to outermost):
# 1. Required headers middleware (runs first)
# 2. CSRF protection middleware (runs second)
# 3. Reboot simulator middleware (runs last)

# Add required headers middleware
app.add_middleware(
    RequiredHeadersMiddleware,
    required_headers={"X-EMC-REST-CLIENT": "true"},
    protected_paths=["/api", "/upload"],
)

# Add CSRF protection middleware
app.add_middleware(
    CSRFProtectionMiddleware,
    excluded_paths=[
        "/api/types/loginSessionInfo/instances",
        "/upload/files/types/candidateSoftwareVersion",
        "/api/auth",
    ],
)

# Add reboot simulator middleware
app.add_middleware(
    RebootSimulatorMiddleware,
    reboot_task_caption="Rebooting the primary SP",
    reset_probability=1.0,  # Always reset during reboot task
)

# Include API routes
app.include_router(router)


# Load persisted state on startup
@app.on_event("startup")
async def startup_event():
    """Load persisted state on startup and restart in-progress upgrade simulations."""
    logger.info("Loading persisted state on startup")

    # Load all state
    import asyncio

    from .models.storage import candidate_software_versions, upgrade_sessions
    from .schemas.base import TaskStatusEnum, UpgradeStatusEnum
    from .utils.state_persistence import load_state
    from .utils.upgrade_simulator import start_upgrade_simulation

    saved_sessions, saved_candidates = load_state()

    # Update candidate software versions first (needed for upgrade sessions)
    if saved_candidates:
        candidate_software_versions.update(saved_candidates)
        logger.info(
            f"Loaded {len(saved_candidates)} candidate software versions from disk"
        )

    # Then update upgrade sessions
    if saved_sessions:
        # Update the in-memory upgrade_sessions with the loaded data
        upgrade_sessions.update(saved_sessions)
        logger.info(f"Loaded {len(saved_sessions)} upgrade sessions from disk")

        # Restart upgrade simulations for in-progress sessions
        in_progress_sessions = []

        for session_id, session in saved_sessions.items():
            session_status = session.get("status")

            # Handle different representations of the status
            if isinstance(session_status, dict) and "_value_" in session_status:
                session_status = session_status["_value_"]
            elif hasattr(session_status, "_value_"):
                session_status = session_status._value_

            # Check if session is in progress or has an in-progress task
            if session_status == UpgradeStatusEnum.IN_PROGRESS or session_status == 1:
                # Check if any task is in progress
                has_in_progress_task = False
                for task in session.get("tasks", []):
                    task_status = (
                        task.get("status")
                        if isinstance(task, dict)
                        else getattr(task, "status", None)
                    )

                    # Handle different representations of the status
                    if isinstance(task_status, dict) and "_value_" in task_status:
                        task_status = task_status["_value_"]
                    elif hasattr(task_status, "_value_"):
                        task_status = task_status._value_

                    if task_status == TaskStatusEnum.IN_PROGRESS or task_status == 1:
                        has_in_progress_task = True
                        break

                if has_in_progress_task:
                    in_progress_sessions.append(session_id)

        if in_progress_sessions:
            logger.info(
                f"Found {len(in_progress_sessions)} in-progress upgrade sessions to restart"
            )

            # Schedule the restart of upgrade simulations after a short delay
            # to ensure the server is fully started
            async def restart_simulations():
                await asyncio.sleep(2)  # Wait for 2 seconds to ensure server is ready
                for session_id in in_progress_sessions:
                    logger.info(
                        f"Restarting upgrade simulation for session {session_id}"
                    )
                    try:
                        # Start the upgrade simulation in the background
                        start_upgrade_simulation(session_id)
                    except Exception as e:
                        logger.error(
                            f"Failed to restart upgrade simulation for session {session_id}: {e}"
                        )

            # Schedule the restart task
            asyncio.create_task(restart_simulations())


# Save state on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    """Save state on shutdown."""
    logger.info("Saving state on shutdown")
    from .models.storage import candidate_software_versions, upgrade_sessions
    from .utils.state_persistence import save_state

    save_state(upgrade_sessions, candidate_software_versions)


def signal_handler(sig, frame):
    """Handle signals to save state before exiting.

    This function ensures that we don't try to save state multiple times
    if multiple signals are received in quick succession.
    """
    # If shutdown is already in progress, just return
    if _shutdown_in_progress.is_set():
        logger.info(f"Shutdown already in progress, ignoring signal {sig}")
        return

    # Set the flag to indicate shutdown is in progress
    _shutdown_in_progress.set()

    logger.info(f"Received signal {sig}, saving state before exiting")
    try:
        from .models.storage import candidate_software_versions, upgrade_sessions
        from .utils.state_persistence import save_state

        SESSION_MESSAGE = (
            f"Saving {len(upgrade_sessions)} upgrade sessions and ",
            f"{len(candidate_software_versions)} candidate software versions",
        )
        # Log the number of sessions being saved
        logger.info(SESSION_MESSAGE)

        # Save the state
        save_state(upgrade_sessions, candidate_software_versions)
        logger.info("State saved successfully")
    except Exception as e:
        logger.error(f"Error saving state: {e}")
    finally:
        # Exit cleanly
        sys.exit(0)


# Register the signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


# Register atexit handler as a fallback
def save_state_on_exit():
    # Only run if shutdown is not already in progress
    if not _shutdown_in_progress.is_set():
        logger.info("atexit handler triggered, saving state")
        try:
            from .models.storage import candidate_software_versions, upgrade_sessions
            from .utils.state_persistence import save_state

            save_state(upgrade_sessions, candidate_software_versions)
            logger.info("State saved successfully by atexit handler")
        except Exception as e:
            logger.error(f"Error saving state in atexit handler: {e}")


atexit.register(save_state_on_exit)


# Run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "dell_unisphere_package.main:app", host="0.0.0.0", port=8000, reload=True
    )
