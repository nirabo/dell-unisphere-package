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

    def test_upload_candidate_software_replaces_existing(
        self, app_client, auth_headers, reset_storage
    ):
        """Test that uploading a new candidate replaces any existing one."""
        # Get CSRF token by making a GET request first
        response = app_client.get(
            "/api/types/loginSessionInfo/instances",
            headers={
                "Authorization": auth_headers["Authorization"],
                "X-EMC-REST-CLIENT": "true",
            },
        )
        assert response.status_code == 200

        # Get CSRF token from cookies
        csrf_token = response.cookies.get("EMC-CSRF-TOKEN")
        assert csrf_token is not None

        # Update headers with CSRF token
        auth_headers["EMC-CSRF-TOKEN"] = csrf_token

        # Set cookies on the client instance
        for cookie_name, cookie_value in response.cookies.items():
            app_client.cookies.set(cookie_name, cookie_value)

        # Upload first candidate
        first_file_content = b"first candidate content"
        first_files = {
            "file": ("first.bin", first_file_content, "application/octet-stream")
        }
        first_response = app_client.post(
            "/upload/files/types/candidateSoftwareVersion",
            files=first_files,
            headers=auth_headers,
        )
        assert first_response.status_code == 200
        first_id = first_response.json()["id"]

        # Verify first candidate exists
        response = app_client.get(
            "/api/types/candidateSoftwareVersion/instances",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["entries"]) == 1
        assert data["entries"][0]["content"]["id"] == first_id

        # Upload second candidate
        second_file_content = b"second candidate content"
        second_files = {
            "file": ("second.bin", second_file_content, "application/octet-stream")
        }
        second_response = app_client.post(
            "/upload/files/types/candidateSoftwareVersion",
            files=second_files,
            headers=auth_headers,
        )
        assert second_response.status_code == 200
        second_id = second_response.json()["id"]

        # Verify only second candidate exists
        response = app_client.get(
            "/api/types/candidateSoftwareVersion/instances",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["entries"]) == 1
        assert data["entries"][0]["content"]["id"] == second_id

    def test_candidate_removal_after_upgrade(
        self, app_client, auth_headers, reset_storage
    ):
        """Test that candidate is removed after successful upgrade."""
        # Get CSRF token by making a GET request first
        response = app_client.get(
            "/api/types/loginSessionInfo/instances",
            headers={
                "Authorization": auth_headers["Authorization"],
                "X-EMC-REST-CLIENT": "true",
            },
        )
        assert response.status_code == 200

        # Get CSRF token from cookies
        csrf_token = response.cookies.get("EMC-CSRF-TOKEN")
        assert csrf_token is not None

        # Update headers with CSRF token
        auth_headers["EMC-CSRF-TOKEN"] = csrf_token

        # Set cookies on the client instance
        for cookie_name, cookie_value in response.cookies.items():
            app_client.cookies.set(cookie_name, cookie_value)

        # Upload a candidate
        file_content = b"test candidate content"
        files = {"file": ("test.bin", file_content, "application/octet-stream")}
        upload_response = app_client.post(
            "/upload/files/types/candidateSoftwareVersion",
            files=files,
            headers=auth_headers,
        )
        assert upload_response.status_code == 200
        candidate_id = upload_response.json()["id"]

        # Create upgrade session
        session_response = app_client.post(
            "/api/types/upgradeSession/instances",
            json={"candidate": candidate_id},
            headers=auth_headers,
        )
        assert session_response.status_code == 200
        session_id = session_response.json()["id"]

        # Start and run the upgrade simulation
        import asyncio
        import time
        from datetime import datetime

        from dell_unisphere_package.models.storage import upgrade_sessions
        from dell_unisphere_package.schemas.base import (
            TaskStatusEnum,
            UpgradeStatusEnum,
        )
        from dell_unisphere_package.utils.upgrade_simulator import (
            process_upgrade_session,
        )

        # Make sure the session exists and set initial status
        session = upgrade_sessions.get(session_id)
        assert session is not None, "Session not found"

        # Create simple test tasks for the upgrade session
        tasks = [
            {
                "id": "task1",
                "caption": "Test Task 1",
                "estimatedTime": "00:00:01.000",
                "status": TaskStatusEnum.PENDING,
                "percentComplete": 0,
            },
            {
                "id": "task2",
                "caption": "Test Task 2",
                "estimatedTime": "00:00:01.000",
                "status": TaskStatusEnum.PENDING,
                "percentComplete": 0,
            },
        ]

        # Set initial session state with all required fields
        session.update(
            {
                "startTime": datetime.now().isoformat(),
                "messages": [],
                "status": UpgradeStatusEnum.IN_PROGRESS,
                "tasks": tasks,
                "percentComplete": 0,
                "elapsedTime": "PT0S",  # ISO 8601 duration format
                "estimatedTotalTime": "PT2S",  # 2 seconds total
            }
        )

        # Run the upgrade process directly in this test
        try:
            # Use a short timeout to run the process_upgrade_session function
            loop = asyncio.get_event_loop()
            task = loop.create_task(process_upgrade_session(session_id))

            # Wait for the upgrade to complete (max 10 seconds)
            max_wait = 10  # seconds
            start_time = time.time()
            while time.time() - start_time < max_wait:
                session = upgrade_sessions.get(session_id)
                if session and session["status"] == UpgradeStatusEnum.COMPLETED:
                    break
                # Give the event loop a chance to run the task
                loop.run_until_complete(asyncio.sleep(0.1))

            # Cancel the task if it's still running
            if not task.done():
                task.cancel()
                try:
                    loop.run_until_complete(task)
                except asyncio.CancelledError:
                    pass
        except Exception as e:
            print(f"Error during upgrade simulation: {e}")

        # Ensure session exists and completed successfully
        session = upgrade_sessions.get(session_id)
        assert session is not None, "Session not found after waiting"
        assert (
            session["status"] == UpgradeStatusEnum.COMPLETED
        ), f"Upgrade did not complete in time. Status: {session['status']}"

        # Verify candidate is removed
        response = app_client.get(
            "/api/types/candidateSoftwareVersion/instances",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["entries"]) == 0

    def test_concurrent_upload_handling(self, app_client, auth_headers, reset_storage):
        """Test that concurrent uploads are handled properly."""
        import asyncio

        from fastapi.testclient import TestClient

        # Get CSRF token by making a GET request first
        response = app_client.get(
            "/api/types/loginSessionInfo/instances",
            headers={
                "Authorization": auth_headers["Authorization"],
                "X-EMC-REST-CLIENT": "true",
            },
        )
        assert response.status_code == 200

        # Get CSRF token from cookies
        csrf_token = response.cookies.get("EMC-CSRF-TOKEN")
        assert csrf_token is not None

        # Update headers with CSRF token
        auth_headers["EMC-CSRF-TOKEN"] = csrf_token

        # Set cookies on the client instance
        for cookie_name, cookie_value in response.cookies.items():
            app_client.cookies.set(cookie_name, cookie_value)

        async def upload_candidate(client: TestClient, headers: dict, file_num: int):
            file_content = f"candidate content {file_num}".encode()
            files = {
                "file": (
                    f"test{file_num}.bin",
                    file_content,
                    "application/octet-stream",
                )
            }
            response = client.post(
                "/upload/files/types/candidateSoftwareVersion",
                files=files,
                headers=headers,
            )
            return response

        async def run_concurrent_uploads():
            # Create multiple upload tasks
            tasks = [upload_candidate(app_client, auth_headers, i) for i in range(5)]
            responses = await asyncio.gather(*tasks)
            return responses

        # Run concurrent uploads
        responses = asyncio.run(run_concurrent_uploads())

        # Verify all uploads were successful
        for response in responses:
            assert response.status_code == 200

        # Verify only one candidate exists
        response = app_client.get(
            "/api/types/candidateSoftwareVersion/instances",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["entries"]) == 1
