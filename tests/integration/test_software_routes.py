"""
Integration tests for software routes.
"""

import pytest


@pytest.mark.integration
class TestSoftwareRoutes:
    """Integration tests for software routes."""

    def test_get_installed_software_versions(
        self, app_client, auth_headers, reset_storage
    ):
        """Test GET /api/types/installedSoftwareVersion/instances returns correct data."""
        # Make the request
        response = app_client.get(
            "/api/types/installedSoftwareVersion/instances", headers=auth_headers
        )

        # Verify response status code
        assert response.status_code == 200

        # Verify response structure
        data = response.json()
        assert "@base" in data
        assert "updated" in data
        assert "links" in data
        assert "entries" in data
        assert len(data["entries"]) > 0

        # Verify entry structure
        entry = data["entries"][0]
        assert "@base" in entry
        assert "content" in entry
        assert "links" in entry
        assert "updated" in entry

        # Verify content
        content = entry["content"]
        assert "id" in content
        assert "version" in content
        assert "revision" in content
        assert "releaseDate" in content
        assert "languages" in content
        assert "hotFixes" in content
        assert "packageVersions" in content
        assert "driveFirmware" in content

        # Verify links
        assert data["links"][0]["rel"] == "self"
        assert entry["links"][0]["rel"] == "self"

    def test_get_installed_software_version_by_id(
        self, app_client, auth_headers, reset_storage
    ):
        """Test GET /api/instances/installedSoftwareVersion/{id} returns correct data."""
        # First get all versions to get a valid ID
        response = app_client.get(
            "/api/types/installedSoftwareVersion/instances", headers=auth_headers
        )
        assert response.status_code == 200

        data = response.json()
        version_id = data["entries"][0]["content"]["id"]

        # Now get the specific version
        response = app_client.get(
            f"/api/instances/installedSoftwareVersion/{version_id}",
            headers=auth_headers,
        )

        # Verify response status code
        assert response.status_code == 200

        # Verify response structure
        data = response.json()
        assert "@base" in data
        assert "content" in data
        assert "links" in data
        assert "updated" in data

        # Verify content
        content = data["content"]
        assert content["id"] == version_id
        assert "version" in content
        assert "revision" in content
        assert "releaseDate" in content
        assert "languages" in content
        assert "hotFixes" in content
        assert "packageVersions" in content
        assert "driveFirmware" in content

    def test_get_installed_software_version_invalid_id(
        self, app_client, auth_headers, reset_storage
    ):
        """Test GET /api/instances/installedSoftwareVersion/{id} with invalid ID returns 404."""
        # Make the request with an invalid ID
        response = app_client.get(
            "/api/instances/installedSoftwareVersion/invalid_id", headers=auth_headers
        )

        # Verify response status code
        assert response.status_code == 404

        # Verify response structure
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_get_installed_software_versions_unauthorized(
        self, app_client, reset_storage
    ):
        """Test GET /api/types/installedSoftwareVersion/instances without auth returns 401."""
        # Make the request without auth headers
        response = app_client.get("/api/types/installedSoftwareVersion/instances")

        # Verify response status code
        assert response.status_code == 401

        # Verify response structure
        data = response.json()
        assert "error" in data

    def test_get_candidate_software_versions(
        self, app_client, auth_headers, reset_storage
    ):
        """Test GET /api/types/candidateSoftwareVersion/instances returns correct data."""
        # Make the request
        response = app_client.get(
            "/api/types/candidateSoftwareVersion/instances", headers=auth_headers
        )

        # Verify response status code
        assert response.status_code == 200

        # Verify response structure
        data = response.json()
        assert "@base" in data
        assert "updated" in data
        assert "links" in data
        assert "entries" in data

        # Note: There might not be any candidate versions initially
        # So we just verify the structure is correct
