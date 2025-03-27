"""Test API server for Dell Unisphere Mock API.

This module provides a standalone FastAPI server that implements the basic endpoints
needed to test the Dell Unisphere API interactions.
"""

import logging
import logging.config

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


# Run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "dell_unisphere_package.main:app", host="0.0.0.0", port=8000, reload=True
    )
