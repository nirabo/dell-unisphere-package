"""
Unit tests for authentication controller functions.
"""

from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException, Request

from dell_unisphere_package.controllers.auth import (
    error_response,
    format_response,
    get_current_user,
)


@pytest.mark.unit
class TestAuthController:
    """Tests for the authentication controller functions."""

    def test_get_current_user_basic_auth_success(self):
        """Test that get_current_user correctly handles HTTP Basic Authentication."""
        # Create a mock request with Basic Auth header
        mock_request = MagicMock(spec=Request)
        mock_request.headers = {
            "Authorization": "Basic YWRtaW46UGFzc3dvcmQxMjMh"
        }  # admin:Password123!
        mock_request.cookies = {}

        # Call the function
        user_info = get_current_user(mock_request)

        # Verify the result
        assert user_info is not None
        assert user_info["username"] == "admin"
        assert "user_id" in user_info
        assert "roles" in user_info
        assert "domain" in user_info

    def test_get_current_user_basic_auth_invalid_credentials(self):
        """Test that get_current_user rejects invalid credentials."""
        # Create a mock request with invalid Basic Auth header
        mock_request = MagicMock(spec=Request)
        mock_request.headers = {
            "Authorization": "Basic aW52YWxpZDppbnZhbGlk"
        }  # invalid:invalid
        mock_request.cookies = {}

        # Call the function and expect an exception
        with pytest.raises(HTTPException) as excinfo:
            get_current_user(mock_request)

        # Verify the exception
        assert excinfo.value.status_code == 401
        assert "Not authenticated" in excinfo.value.detail

    def test_get_current_user_session_auth_success(self):
        """Test that get_current_user correctly handles session-based authentication."""
        # Create a mock request with session cookie
        mock_request = MagicMock(spec=Request)
        mock_request.headers = {}

        # Create a test session
        from dell_unisphere_package.models.storage import sessions

        session_id = "test-session-id"
        sessions[session_id] = {
            "username": "admin",
            "user_id": "user_1",
            "roles": ["administrator"],
            "domain": "Local",
        }

        mock_request.cookies = {"EMC-CSRF-TOKEN": session_id}

        # Call the function
        user_info = get_current_user(mock_request)

        # Verify the result
        assert user_info is not None
        assert user_info["username"] == "admin"
        assert user_info["user_id"] == "user_1"
        assert "administrator" in user_info["roles"]
        assert user_info["domain"] == "Local"

        # Clean up
        del sessions[session_id]

    def test_get_current_user_no_auth(self):
        """Test that get_current_user rejects requests with no authentication."""
        # Create a mock request with no auth
        mock_request = MagicMock(spec=Request)
        mock_request.headers = {}
        mock_request.cookies = {}

        # Call the function and expect an exception
        with pytest.raises(HTTPException) as excinfo:
            get_current_user(mock_request)

        # Verify the exception
        assert excinfo.value.status_code == 401
        assert "Not authenticated" in excinfo.value.detail

    def test_format_response_collection(self):
        """Test that format_response correctly formats a collection response."""
        # Create test data
        data = [{"id": "1", "name": "Item 1"}, {"id": "2", "name": "Item 2"}]

        # Create a mock request
        mock_request = MagicMock(spec=Request)
        mock_request.url.scheme = "http"
        mock_request.url.netloc = "localhost:8000"

        # Call the function
        response = format_response(data, mock_request, instance_type="test")

        # Verify the response structure
        assert "@base" in response
        assert "updated" in response
        assert "links" in response
        assert "entries" in response
        assert len(response["entries"]) == 2

        # Verify entry structure
        entry = response["entries"][0]
        assert "@base" in entry
        assert "content" in entry
        assert "links" in entry
        assert "updated" in entry

        # Verify links
        assert response["links"][0]["rel"] == "self"
        assert entry["links"][0]["rel"] == "self"

    def test_format_response_instance(self):
        """Test that format_response correctly formats a single instance response."""
        # Create test data
        data = {"id": "1", "name": "Item 1"}

        # Create a mock request
        mock_request = MagicMock(spec=Request)
        mock_request.url.scheme = "http"
        mock_request.url.netloc = "localhost:8000"

        # Call the function
        response = format_response(
            data, mock_request, instance_type="test", instance_id="1"
        )

        # Verify the response structure
        assert "@base" in response
        assert "content" in response
        assert "links" in response
        assert "updated" in response

        # Verify links
        assert response["links"][0]["rel"] == "self"
        assert response["links"][0]["href"] == "/1"

    def test_error_response(self):
        """Test that error_response correctly formats error responses."""
        # Call the function for different error codes
        bad_request = error_response(400, "Bad request message")
        unauthorized = error_response(401, "Unauthorized message")
        not_found = error_response(404, "Not found message")
        server_error = error_response(500, "Server error message")

        # Verify the response structure
        for response in [bad_request, unauthorized, not_found, server_error]:
            assert "errorCode" in response
            assert "httpStatusCode" in response
            assert "messages" in response
            assert len(response["messages"]) == 1
            assert "en-US" in response["messages"][0]

        # Verify specific error codes
        assert bad_request["httpStatusCode"] == 400
        assert unauthorized["httpStatusCode"] == 401
        assert not_found["httpStatusCode"] == 404
        assert server_error["httpStatusCode"] == 500

        # Verify error messages
        assert bad_request["messages"][0]["en-US"] == "Bad request message"
        assert unauthorized["messages"][0]["en-US"] == "Unauthorized message"
        assert not_found["messages"][0]["en-US"] == "Not found message"
        assert server_error["messages"][0]["en-US"] == "Server error message"
