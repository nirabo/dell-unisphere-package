"""
Integration tests for system routes.
"""

import pytest


@pytest.mark.integration
class TestSystemRoutes:
    """Integration tests for system routes."""

    def test_get_basic_system_info(self, app_client, reset_storage):
        """Test GET /api/types/basicSystemInfo/instances returns correct data."""
        # Make the request
        response = app_client.get(
            "/api/types/basicSystemInfo/instances",
            headers={"X-EMC-REST-CLIENT": "true"},
        )

        # Verify response status code
        assert response.status_code == 200

        # Verify response structure
        data = response.json()
        assert "@base" in data
        assert "updated" in data
        assert "links" in data
        assert "entries" in data
        assert len(data["entries"]) == 1

        # Verify entry structure
        entry = data["entries"][0]
        assert "@base" in entry
        assert "content" in entry
        assert "links" in entry
        assert "updated" in entry

        # Verify content
        content = entry["content"]
        assert content["id"] == "0"
        assert content["model"] == "Unity 380F"
        assert content["name"] == "CKM01204905476"
        assert content["softwareVersion"] == "5.3.0"
        assert "Unity 5.3.0.0" in content["softwareFullVersion"]
        assert content["apiVersion"] == "13.0"
        assert content["earliestApiVersion"] == "4.0"

        # Verify links
        assert data["links"][0]["rel"] == "self"
        assert entry["links"][0]["rel"] == "self"

        # Verify response headers
        assert response.headers["Content-Type"] == "application/json"

    def test_get_basic_system_info_no_auth_required(self, app_client, reset_storage):
        """Test that GET /api/types/basicSystemInfo/instances doesn't require authentication."""
        # Make the request without auth headers but with the required REST client header
        response = app_client.get(
            "/api/types/basicSystemInfo/instances",
            headers={"X-EMC-REST-CLIENT": "true"},
        )

        # Verify response status code
        assert response.status_code == 200

        # Verify we got valid data
        data = response.json()
        assert "entries" in data
        assert len(data["entries"]) == 1
