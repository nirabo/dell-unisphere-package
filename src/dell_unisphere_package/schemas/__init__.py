"""Schemas package for Dell Unisphere API.

This package contains all the Pydantic models used for data validation and serialization.
"""

from .base import (
    BasicSystemInfo,
    User,
    Role,
    LoginSessionInfo,
    UpgradeTypeEnum,
    UpgradeStatusEnum,
    UpgradeSessionTypeEnum,
    TaskStatusEnum,
    TaskTypeEnum,
)

from .upgrade import (
    CandidateSoftwareVersion,
    UpgradeTask,
    UpgradeMessage,
    UpgradeSession,
)

__all__ = [
    "BasicSystemInfo",
    "User",
    "Role",
    "LoginSessionInfo",
    "UpgradeTypeEnum",
    "UpgradeStatusEnum",
    "UpgradeSessionTypeEnum",
    "TaskStatusEnum",
    "TaskTypeEnum",
    "CandidateSoftwareVersion",
    "UpgradeTask",
    "UpgradeMessage",
    "UpgradeSession",
]
