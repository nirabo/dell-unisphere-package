"""Storage models for Dell Unisphere API.

This module provides in-memory storage for the API.
"""

from datetime import datetime, timedelta
from typing import Any, Dict

# In-memory storage
sessions: Dict[str, Any] = {}
users = {
    "admin": {
        "id": "user_admin",
        "password": "Password123!",
        "roles": [{"id": "administrator"}],
        "domain": "local",
    },
    "user": {
        "id": "user_user",
        "password": "Password123!",
        "roles": [{"id": "user"}],
        "domain": "local",
    },
    "diagnose": {
        "id": "user_diagnose",
        "password": "Password123!",
        "roles": [{"id": "diagnose"}],
        "domain": "local",
    },
}
# Initially empty, will be populated when software is uploaded and prepared
candidate_software_versions: Dict[str, Any] = {}
upgrade_sessions = {
    "Upgrade_4.3.0.1499782821": {
        "id": "Upgrade_4.3.0.1499782821",
        "type": 0,  # UPGRADE
        "candidate": "candidate_default",
        "caption": "Upgrade_4.3.0.1499782821",
        "status": 2,  # COMPLETED
        "messages": [],
        "creationTime": (datetime.now() - timedelta(days=30)).isoformat(),
        "elapsedTime": "PT2H30M",
        "percentComplete": 100,
        "tasks": [],
    }
}
uploaded_files: Dict[str, Any] = {}

# Installed software versions
installed_software_versions = {
    "0": {
        "id": "0",
        "version": "5.3.0",
        "revision": 120,
        "releaseDate": datetime.now().isoformat(),
        "fullVersion": "Unity 5.3.0.0 (Release, Build 120, 2023-03-18 19:02:01, 5.3.0.0.5.120)",
        "languages": [
            {"name": "English", "version": "5.3.0"},
            {"name": "Chinese", "version": "5.3.0"},
        ],
        "hotFixes": ["HF1", "HF2"],
        "packageVersions": [
            {"name": "Base", "version": "5.3.0"},
            {"name": "Management", "version": "5.3.0"},
        ],
        "driveFirmware": [
            {
                "name": "Drive Firmware Package 1",
                "version": "1.2.3",
                "releaseDate": datetime.now().isoformat(),
                "upgradedeDriveCount": 24,
                "estimatedTime": 30,
                "isNewVersion": False,
            }
        ],
    }
}
