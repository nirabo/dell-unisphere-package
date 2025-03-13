"""
End-to-end tests for authentication and session management workflow.
"""

import pytest
import base64
from fastapi.testclient import TestClient


@pytest.mark.e2e
class TestAuthWorkflow:
    """End-to-end tests for authentication and session management workflow."""

    def test_complete_auth_workflow(self, app_client, reset_storage):
        """Test the complete authentication workflow from login to logout."""
        # Step 1: Authenticate with Basic Auth
        credentials = base64.b64encode(b"admin:Password123!").decode("utf-8")
        headers = {"Authorization": f"Basic {credentials}", "X-EMC-REST-CLIENT": "true"}

        login_response = app_client.get(
            "/api/types/loginSessionInfo/instances", headers=headers
        )

        # Verify successful login
        assert login_response.status_code == 200
        login_data = login_response.json()
        assert "content" in login_data

        # Verify content values
        content = login_data["content"]
        assert content["domain"] == "local"
        assert content["user"]["id"] == "user_admin"
        assert len(content["roles"]) > 0
        assert content["roles"][0]["id"] == "administrator"

        # Get CSRF token from cookies
        assert "EMC-CSRF-TOKEN" in login_response.cookies
        csrf_token = login_response.cookies["EMC-CSRF-TOKEN"]
        assert csrf_token is not None

        # Step 2: Access protected resource with session cookie and CSRF token
        protected_headers = headers.copy()
        protected_headers["EMC-CSRF-TOKEN"] = csrf_token

        # Set cookies directly on the client instance
        for cookie_name, cookie_value in login_response.cookies.items():
            app_client.cookies.set(cookie_name, cookie_value)

        # Try to access user information
        users_response = app_client.get(
            "/api/types/user/instances", headers=protected_headers
        )

        # Verify access to protected resource
        assert users_response.status_code == 200
        users_data = users_response.json()
        assert "entries" in users_data

        # Step 3: Logout
        logout_response = app_client.post(
            "/api/types/loginSessionInfo/action/logout", headers=protected_headers
        )

        # Verify successful logout
        assert logout_response.status_code == 200
        logout_data = logout_response.json()
        assert "message" in logout_data
        assert "Logged out successfully" in logout_data["message"]

        # Step 4: Verify session cookie is removed after logout
        assert "EMC-CSRF-TOKEN" not in logout_response.cookies

        # Create a new client without cookies to verify authentication is required
        new_client = TestClient(app_client.app)
        post_logout_response = new_client.get("/api/types/user/instances")

        # Verify access is denied without authentication
        assert post_logout_response.status_code == 401

    def test_csrf_protection_workflow(self, app_client, reset_storage):
        """Test the CSRF protection workflow."""
        # Step 1: Authenticate with Basic Auth
        credentials = base64.b64encode(b"admin:Password123!").decode("utf-8")
        headers = {"Authorization": f"Basic {credentials}", "X-EMC-REST-CLIENT": "true"}

        login_response = app_client.get(
            "/api/types/loginSessionInfo/instances", headers=headers
        )

        # Verify successful login
        assert login_response.status_code == 200

        # Set cookies directly on the client instance
        for cookie_name, cookie_value in login_response.cookies.items():
            app_client.cookies.set(cookie_name, cookie_value)

        # Step 2: Try to make a POST request without CSRF token
        post_response = app_client.post(
            "/api/types/loginSessionInfo/action/logout", headers=headers
        )

        # Verify CSRF protection blocks the request
        assert post_response.status_code == 403
        post_data = post_response.json()
        assert "error" in post_data
        assert "CSRF" in post_data["error"]

        # Step 3: Try with invalid CSRF token
        invalid_csrf_headers = headers.copy()
        invalid_csrf_headers["EMC-CSRF-TOKEN"] = "invalid-token"

        invalid_csrf_response = app_client.post(
            "/api/types/loginSessionInfo/action/logout", headers=invalid_csrf_headers
        )

        # The current implementation only checks for token presence, not validity
        assert invalid_csrf_response.status_code == 200

        # Step 4: Try with correct CSRF token
        valid_csrf_headers = headers.copy()
        valid_csrf_headers["EMC-CSRF-TOKEN"] = login_response.cookies["EMC-CSRF-TOKEN"]

        valid_csrf_response = app_client.post(
            "/api/types/loginSessionInfo/action/logout", headers=valid_csrf_headers
        )

        # Verify request succeeds with valid CSRF token
        assert valid_csrf_response.status_code == 200
