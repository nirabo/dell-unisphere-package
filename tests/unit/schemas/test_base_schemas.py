"""
Unit tests for base schemas.
"""

import pytest

from dell_unisphere_package.schemas.base import (
    BasicSystemInfo,
    # LoginSessionInfo,
    # User,
    # Role,
    InstalledSoftwareVersion,
    InstalledSoftwareVersionLanguage,
    InstalledSoftwareVersionPackage,
    FirmwarePackage,
)


@pytest.mark.unit
class TestBasicSystemInfo:
    """Tests for the BasicSystemInfo schema."""

    def test_basic_system_info_default_values(self):
        """Test that BasicSystemInfo has the expected default values."""
        info = BasicSystemInfo()
        assert info.id == "0"
        assert info.model == "Unity 380F"
        assert info.name == "CKM01204905476"
        assert info.softwareVersion == "5.3.0"
        assert "Unity 5.3.0.0" in info.softwareFullVersion
        assert info.apiVersion == "13.0"
        assert info.earliestApiVersion == "4.0"

    def test_basic_system_info_custom_values(self):
        """Test that BasicSystemInfo accepts custom values."""
        custom_info = BasicSystemInfo(
            id="1",
            model="Unity 500F",
            name="TestSystem",
            softwareVersion="5.4.0",
            softwareFullVersion="Unity 5.4.0.0 (Release, Build 150, 2024-01-01 12:00:00, 5.4.0.0.5.150)",
            apiVersion="14.0",
            earliestApiVersion="5.0",
        )
        assert custom_info.id == "1"
        assert custom_info.model == "Unity 500F"
        assert custom_info.name == "TestSystem"
        assert custom_info.softwareVersion == "5.4.0"
        assert "Unity 5.4.0.0" in custom_info.softwareFullVersion
        assert custom_info.apiVersion == "14.0"
        assert custom_info.earliestApiVersion == "5.0"


@pytest.mark.unit
class TestInstalledSoftwareVersion:
    """Tests for the InstalledSoftwareVersion schema."""

    def test_installed_software_version_default_values(self):
        """Test that InstalledSoftwareVersion has the expected default values."""
        version = InstalledSoftwareVersion()
        assert version.id == "0"
        assert version.version == "5.3.0"
        assert version.revision == 120
        assert version.fullVersion is not None
        assert len(version.languages) == 2
        assert len(version.hotFixes) == 2
        assert len(version.packageVersions) == 2
        assert len(version.driveFirmware) == 1

    def test_installed_software_version_language(self):
        """Test the InstalledSoftwareVersionLanguage embedded schema."""
        language = InstalledSoftwareVersionLanguage(name="Spanish", version="5.3.0")
        assert language.name == "Spanish"
        assert language.version == "5.3.0"

    def test_installed_software_version_package(self):
        """Test the InstalledSoftwareVersionPackage embedded schema."""
        package = InstalledSoftwareVersionPackage(name="Security", version="5.3.0")
        assert package.name == "Security"
        assert package.version == "5.3.0"

    def test_firmware_package(self):
        """Test the FirmwarePackage embedded schema."""
        from datetime import datetime

        release_date = datetime.now()
        firmware = FirmwarePackage(
            name="Drive Firmware Package 2",
            version="2.0.0",
            releaseDate=release_date,
            upgradedeDriveCount=10,
            estimatedTime=15,
            isNewVersion=True,
        )

        assert firmware.name == "Drive Firmware Package 2"
        assert firmware.version == "2.0.0"
        assert firmware.releaseDate == release_date
        assert firmware.upgradedeDriveCount == 10
        assert firmware.estimatedTime == 15
        assert firmware.isNewVersion is True
