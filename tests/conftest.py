"""
Global pytest fixtures and configuration.
"""

import os
import pytest
from fastapi.testclient import TestClient

from dell_unisphere_package.main import app
from dell_unisphere_package.models.storage import (
    users,
    sessions,
    candidate_software_versions,
    upgrade_sessions,
)


@pytest.fixture
def app_client():
    """
    Create a FastAPI TestClient instance for testing API endpoints.
    """
    return TestClient(app)


@pytest.fixture
def reset_storage():
    """
    Reset in-memory storage before and after tests.
    """
    # Store original data
    original_users = users.copy()
    original_sessions = sessions.copy()
    original_candidate_versions = candidate_software_versions.copy()
    original_upgrade_sessions = upgrade_sessions.copy()

    # Clear for test
    users.clear()
    sessions.clear()
    candidate_software_versions.clear()
    upgrade_sessions.clear()

    # Add default test users
    users["admin"] = {
        "id": "user_1",
        "username": "admin",
        "password": "Password123!",
        "roles": ["administrator"],
        "domain": "Local",
    }
    users["user"] = {
        "id": "user_2",
        "username": "user",
        "password": "Password123!",
        "roles": ["operator"],
        "domain": "Local",
    }

    yield

    # Restore original data
    users.clear()
    sessions.clear()
    candidate_software_versions.clear()
    upgrade_sessions.clear()

    users.update(original_users)
    sessions.update(original_sessions)
    candidate_software_versions.update(original_candidate_versions)
    upgrade_sessions.update(original_upgrade_sessions)


@pytest.fixture
def auth_headers():
    """
    Return headers with HTTP Basic Authentication.
    """
    import base64

    credentials = base64.b64encode(b"admin:Password123!").decode("utf-8")
    return {"Authorization": f"Basic {credentials}", "X-EMC-REST-CLIENT": "true"}


@pytest.fixture
def csrf_token(app_client, auth_headers):
    """
    Get a valid CSRF token for testing protected endpoints.
    """
    response = app_client.get(
        "/api/types/loginSessionInfo/instances", headers=auth_headers
    )
    assert response.status_code == 200

    # Extract CSRF token from cookies
    cookies = response.cookies
    csrf_token = cookies.get("EMC-CSRF-TOKEN")
    assert csrf_token is not None

    return csrf_token


@pytest.fixture
def mock_file(tmp_path):
    """
    Create a mock file for testing file uploads.
    """
    file_path = tmp_path / "test_upgrade.bin"
    with open(file_path, "wb") as f:
        f.write(os.urandom(1024))  # 1KB test file

    return file_path
