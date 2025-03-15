"""
Integration tests for authentication routes.
"""

import base64

import pytest


@pytest.mark.integration
class TestAuthRoutes:
    """Integration tests for authentication routes."""

    def test_login_session_info_valid_credentials(self, app_client, reset_storage):
        """Test GET /api/types/loginSessionInfo/instances with valid credentials."""
        # Create auth headers
        credentials = base64.b64encode(b"admin:Password123!").decode("utf-8")
        headers = {"Authorization": f"Basic {credentials}", "X-EMC-REST-CLIENT": "true"}

        # Make the request
        response = app_client.get(
            "/api/types/loginSessionInfo/instances", headers=headers
        )

        # Verify response status code
        assert response.status_code == 200

        # Verify response structure
        data = response.json()
        assert "@base" in data
        assert "content" in data
        assert "links" in data
        assert "updated" in data

        # Verify content structure
        content = data["content"]
        assert "domain" in content
        assert "id" in content
        assert "roles" in content
        assert "user" in content

        # Verify content values
        assert content["domain"] == "local"
        assert content["id"] is not None
        assert len(content["roles"]) > 0
        assert content["roles"][0]["id"] == "administrator"
        assert content["user"]["id"] == "user_admin"

        # Verify cookies
        assert "EMC-CSRF-TOKEN" in response.cookies
        csrf_token = response.cookies["EMC-CSRF-TOKEN"]
        assert csrf_token is not None
        assert csrf_token != ""

    def test_login_session_info_invalid_credentials(self, app_client, reset_storage):
        """Test GET /api/types/loginSessionInfo/instances with invalid credentials."""
        # Create auth headers with invalid credentials
        credentials = base64.b64encode(b"invalid:invalid").decode("utf-8")
        headers = {"Authorization": f"Basic {credentials}", "X-EMC-REST-CLIENT": "true"}

        # Make the request
        response = app_client.get(
            "/api/types/loginSessionInfo/instances", headers=headers
        )

        # Verify response status code
        assert response.status_code == 401

        # Verify response structure
        data = response.json()
        assert "detail" in data
        assert (
            "Not authenticated" in data["detail"]
            or "Missing or invalid" in data["detail"]
        )

        # Verify no cookies
        assert "EMC-CSRF-TOKEN" not in response.cookies

    def test_login_session_info_missing_auth(self, app_client, reset_storage):
        """Test GET /api/types/loginSessionInfo/instances with no authentication."""
        # Make the request without auth headers
        response = app_client.get(
            "/api/types/loginSessionInfo/instances",
            headers={"X-EMC-REST-CLIENT": "true"},
        )

        # Verify response status code
        assert response.status_code == 401

        # Verify response structure
        data = response.json()
        assert "detail" in data
        assert (
            "Not authenticated" in data["detail"]
            or "Missing or invalid" in data["detail"]
        )

    def test_logout(self, app_client, auth_headers, csrf_token, reset_storage):
        """Test POST /api/types/loginSessionInfo/action/logout."""
        # Add CSRF token to headers
        headers = auth_headers.copy()
        headers["EMC-CSRF-TOKEN"] = csrf_token

        # Make the request
        response = app_client.post(
            "/api/types/loginSessionInfo/action/logout", headers=headers
        )

        # Verify response status code
        assert response.status_code == 200

        # Verify response structure
        data = response.json()
        assert "message" in data
        assert "Logged out successfully" in data["message"]

        # No need to check cookies as they are handled by the client

    def test_csrf_protection(self, app_client, auth_headers, csrf_token, reset_storage):
        """Test that POST requests require a valid CSRF token."""
        # Make the request without CSRF token
        response = app_client.post(
            "/api/types/loginSessionInfo/action/logout", headers=auth_headers
        )

        # Verify response status code
        assert response.status_code == 403

        # Verify response structure
        data = response.json()
        assert "error" in data
        assert "CSRF" in data["error"]
