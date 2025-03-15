"""Upgrade schemas for Dell Unisphere API.

This module defines the Pydantic models related to software upgrades.
"""

from datetime import datetime, timedelta
from typing import List

from pydantic import BaseModel

from .base import (
    TaskStatusEnum,
    TaskTypeEnum,
    UpgradeSessionTypeEnum,
    UpgradeStatusEnum,
    UpgradeTypeEnum,
)


class CandidateSoftwareVersion(BaseModel):
    id: str
    version: str
    fullVersion: str
    revision: int
    releaseDate: datetime
    type: UpgradeTypeEnum = UpgradeTypeEnum.SOFTWARE
    rebootRequired: bool = True
    canPauseBeforeReboot: bool = True


class UpgradeTask(BaseModel):
    status: TaskStatusEnum
    type: TaskTypeEnum
    caption: str
    creationTime: datetime
    estRemainTime: str = "00:03:30.000"


class UpgradeMessage(BaseModel):
    timestamp: datetime
    message: str
    severity: int = 0


class UpgradeSession(BaseModel):
    id: str
    type: UpgradeSessionTypeEnum = UpgradeSessionTypeEnum.UPGRADE
    candidate: str  # Reference to CandidateSoftwareVersion id
    caption: str
    status: UpgradeStatusEnum
    messages: List[UpgradeMessage] = []
    creationTime: datetime
    elapsedTime: timedelta = timedelta(minutes=0)
    percentComplete: int = 0
    tasks: List[UpgradeTask] = []
