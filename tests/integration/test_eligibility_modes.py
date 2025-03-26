"""Integration tests for the eligibility endpoint in different modes."""

import logging

import pytest

from dell_unisphere_package.models.storage import system_config

# Set up logger
logger = logging.getLogger(__name__)


@pytest.mark.integration
class TestEligibilityModes:
    """Integration tests for eligibility endpoint in different modes."""

    @pytest.fixture(autouse=True)
    def reset_system_config(self):
        """Reset system configuration to default after each test."""
        # Store original configuration
        original_config = system_config.copy()

        yield

        # Restore original configuration after test
        for key, value in original_config.items():
            system_config[key] = value

    @pytest.fixture
    def csrf_token(self, app_client, auth_headers):
        """Get a CSRF token for the test."""
        # Login to get a CSRF token
        login_response = app_client.get(
            "/api/types/loginSessionInfo/instances", headers=auth_headers
        )
        assert login_response.status_code == 200

        # Extract the CSRF token from cookies
        csrf_token = login_response.cookies.get("EMC-CSRF-TOKEN")
        assert csrf_token is not None

        return csrf_token

    def test_get_system_config(self, app_client, auth_headers):
        """Test getting the current system configuration."""
        response = app_client.get(
            "/api/types/systemConfig/instances", headers=auth_headers
        )
        assert response.status_code == 200

        data = response.json()
        assert "content" in data
        assert "eligibility_status" in data["content"]
        assert "failure_codes" in data["content"]
        assert "auto_failure_threshold" in data["content"]

    def test_update_system_config(self, app_client, auth_headers, csrf_token):
        """Test updating the system configuration."""
        headers = {**auth_headers, "EMC-CSRF-TOKEN": csrf_token}

        # Update to failure mode
        response = app_client.post(
            "/api/types/systemConfig/action/update",
            json={"eligibility_status": "failure"},
            headers=headers,
        )
        assert response.status_code == 200

        # Verify update was successful
        data = response.json()
        assert data["content"]["eligibility_status"] == "failure"

        # Verify system_config was updated
        assert system_config["eligibility_status"] == "failure"

    @pytest.mark.parametrize(
        "eligibility_status,expected_status",
        [
            ("success", False),  # success mode: overallStatus should be False
            ("failure", True),  # failure mode: overallStatus should be True
        ],
    )
    def test_eligibility_system_config_modes(
        self, app_client, auth_headers, csrf_token, eligibility_status, expected_status
    ):
        """Test eligibility endpoint with different system configuration modes."""
        headers = {**auth_headers, "EMC-CSRF-TOKEN": csrf_token}

        # Set system config to the specified mode
        app_client.post(
            "/api/types/systemConfig/action/update",
            json={"eligibility_status": eligibility_status},
            headers=headers,
        )

        # Test eligibility endpoint
        response = app_client.post(
            "/api/types/upgradeSession/action/verifyUpgradeEligibility",
            headers=headers,
        )
        assert response.status_code == 200

        # Verify response structure matches expected status
        data = response.json()
        assert "updated" in data
        assert "content" in data

        if expected_status:  # Failure case
            assert "codes" in data["content"]
            assert "messages" in data["content"]
            assert data["content"]["overallStatus"] is True
        else:  # Success case
            assert "statusMessage" in data["content"]
            assert data["content"]["statusMessage"] == ""
            assert data["content"]["overallStatus"] is False

    @pytest.mark.parametrize(
        "fail_param,expected_status",
        [
            (False, False),  # explicit success: overallStatus should be False
            (True, True),  # explicit failure: overallStatus should be True
        ],
    )
    def test_eligibility_explicit_parameter(
        self, app_client, auth_headers, csrf_token, fail_param, expected_status
    ):
        """Test eligibility endpoint with explicit parameter override."""
        headers = {**auth_headers, "EMC-CSRF-TOKEN": csrf_token}

        # Set system config to the opposite of what we're testing with the parameter
        # This ensures the parameter is actually overriding the system config
        opposite_status = "failure" if fail_param is False else "success"
        app_client.post(
            "/api/types/systemConfig/action/update",
            json={"eligibility_status": opposite_status},
            headers=headers,
        )

        # Test eligibility endpoint with explicit parameter
        response = app_client.post(
            f"/api/types/upgradeSession/action/verifyUpgradeEligibility?fail={str(fail_param).lower()}",
            headers=headers,
        )
        assert response.status_code == 200

        # Verify response structure matches expected status
        data = response.json()
        assert "updated" in data
        assert "content" in data

        if expected_status:  # Failure case
            assert "codes" in data["content"]
            assert "messages" in data["content"]
            assert data["content"]["overallStatus"] is True
        else:  # Success case
            assert "statusMessage" in data["content"]
            assert data["content"]["statusMessage"] == ""
            assert data["content"]["overallStatus"] is False

    def test_auto_mode_randomness(self, app_client, auth_headers, csrf_token):
        """Test that auto mode produces both success and failure responses."""
        headers = {**auth_headers, "EMC-CSRF-TOKEN": csrf_token}

        # Set system to auto mode with 50% failure rate
        app_client.post(
            "/api/types/systemConfig/action/update",
            json={"eligibility_status": "auto", "auto_failure_threshold": 0.5},
            headers=headers,
        )

        # Run multiple tests to ensure we get both success and failure responses
        success_count = 0
        failure_count = 0
        total_runs = 20

        for _ in range(total_runs):
            response = app_client.post(
                "/api/types/upgradeSession/action/verifyUpgradeEligibility",
                headers=headers,
            )
            assert response.status_code == 200

            data = response.json()
            if "statusMessage" in data["content"]:
                success_count += 1
            else:
                failure_count += 1

        # With 20 runs and 50% probability, it's extremely unlikely to get all successes or all failures
        # This is a probabilistic test, but should be reliable enough
        assert success_count > 0, "Expected some success responses in auto mode"
        assert failure_count > 0, "Expected some failure responses in auto mode"

        logger.info(
            f"Auto mode test: {success_count} successes, {failure_count} failures out of {total_runs} runs"
        )
