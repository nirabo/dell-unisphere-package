"""Base schemas for Dell Unisphere API.

This module defines the Pydantic models used for data validation and serialization.
"""

from typing import List
from enum import Enum
from pydantic import BaseModel


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
    roles: List[Role]
    domain: str
    user: User
    id: str
    idleTimeout: int = 3600
    isPasswordChangeRequired: bool = False


class UpgradeTypeEnum(str, Enum):
    SOFTWARE = "SOFTWARE"
    LANGUAGE_PACK = "LANGUAGE_PACK"


class UpgradeStatusEnum(int, Enum):
    PENDING = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    FAILED = 3
    PAUSED = 4


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
