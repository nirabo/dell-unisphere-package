"""Base schemas for Dell Unisphere API.

This module defines the Pydantic models used for data validation and serialization.
"""

from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class BasicSystemInfo(BaseModel):
    id: str = "0"
    model: str = "Unity 380F"
    name: str = "CKM01204905476"
    softwareVersion: str = "5.3.0"
    softwareFullVersion: str = (
        "Unity 5.3.0.0 (Release, Build 120, 2023-03-18 19:02:01, 5.3.0.0.5.120)"
    )
    apiVersion: str = "13.0"
    earliestApiVersion: str = "4.0"


class User(BaseModel):
    id: str


class Role(BaseModel):
    id: str


class LoginSessionInfo(BaseModel):
    domain: str
    idleTimeout: int = 3600
    roles: list[Role] = []
    user: User = None
    id: str
    isPasswordChangeRequired: bool = False


class UpgradeTypeEnum(str, Enum):
    SOFTWARE = "SOFTWARE"
    LANGUAGE_PACK = "LANGUAGE_PACK"


class UpgradeStatusEnum(int, Enum):
    NOT_STARTED = 0  # Upgrade_Not_Started
    IN_PROGRESS = 1  # Upgrade_in_Progress
    COMPLETED = 2  # Upgrade_Completed
    FAILED = 3  # Upgrade_Failed
    FAILED_LOCK = 4  # Upgrade_Failed_Lock
    CANCELLED = 5  # Upgrade_Cancelled
    PAUSED = 6  # Upgrade_Paused
    ACKNOWLEDGED = 7  # Upgrade_Acknowledged
    WAITING_FOR_USER = 8  # Upgrade_Waiting_For_User
    PAUSED_LOCK = 9  # Upgrade_Paused_Lock


class UpgradeSessionTypeEnum(int, Enum):
    UPGRADE = 0
    INSTALL = 1


class TaskStatusEnum(int, Enum):
    PENDING = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    FAILED = 3
    PAUSED = 4


class TaskTypeEnum(int, Enum):
    PREPARE = 0
    UPLOAD = 1
    INSTALL = 2
    REBOOT = 3


class FirmwarePackage(BaseModel):
    name: str
    version: str
    releaseDate: datetime
    upgradedeDriveCount: int = Field(
        0, description="The number of upgraded drives in the array"
    )
    estimatedTime: int = Field(
        0, description="Time estimation to upgrade drive firmware in minutes"
    )
    isNewVersion: bool = Field(
        False,
        description="Indicates whether the drive firmware package is newer than the installed one",
    )


class InstalledSoftwareVersionLanguage(BaseModel):
    name: str
    version: str


class InstalledSoftwareVersionPackage(BaseModel):
    name: str
    version: str


class InstalledSoftwareVersion(BaseModel):
    id: str = "0"
    version: str = "5.3.0"
    revision: int = 120
    releaseDate: datetime = datetime.now()
    fullVersion: str = (
        "Unity 5.3.0.0 (Release, Build 120, 2023-03-18 19:02:01, 5.3.0.0.5.120)"
    )
    languages: List[InstalledSoftwareVersionLanguage] = [
        InstalledSoftwareVersionLanguage(name="English", version="5.3.0"),
        InstalledSoftwareVersionLanguage(name="Chinese", version="5.3.0"),
    ]
    hotFixes: List[str] = ["HF1", "HF2"]
    packageVersions: List[InstalledSoftwareVersionPackage] = [
        InstalledSoftwareVersionPackage(name="Base", version="5.3.0"),
        InstalledSoftwareVersionPackage(name="Management", version="5.3.0"),
    ]
    driveFirmware: List[FirmwarePackage] = [
        FirmwarePackage(
            name="Drive Firmware Package 1",
            version="1.2.3",
            releaseDate=datetime.now(),
            upgradedeDriveCount=24,
            estimatedTime=30,
            isNewVersion=False,
        )
    ]
