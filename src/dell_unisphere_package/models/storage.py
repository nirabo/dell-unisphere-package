"""Storage models for Dell Unisphere API.

This module provides in-memory storage for the API.
"""

from datetime import datetime, timedelta
from typing import Dict, Any

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
