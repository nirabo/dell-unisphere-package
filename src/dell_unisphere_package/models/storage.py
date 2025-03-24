"""Thread-safe storage models for Dell Unisphere API.

This module provides persistent storage for the API using a JSON file-based database
with thread-safe operations using threading.Lock.
"""

import json
import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class Storage:
    """Thread-safe JSON file-based storage implementation."""

    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.lock = threading.Lock()
        self._initialize_db()

    def _initialize_db(self) -> None:
        """Initialize the database file if it doesn't exist."""
        if not self.db_path.exists():
            with self.lock:
                self.db_path.parent.mkdir(parents=True, exist_ok=True)
                self._write_db(
                    {
                        "system": {},
                        "users": {},
                        "candidate_software_versions": {},
                        "version_history": [],
                        "sessions": {},
                        "upgrade_sessions": {},
                        "uploaded_files": {},
                    }
                )

    def _read_db(self) -> Dict[str, Any]:
        """Read the entire database with thread safety."""
        with self.lock:
            with open(self.db_path, "r") as f:
                return json.load(f)

    def _write_db(self, data: Dict[str, Any]) -> None:
        """Write to the database with thread safety."""
        with self.lock:
            with open(self.db_path, "w") as f:
                json.dump(data, f, indent=2)

    def get_collection(self, collection_name: str) -> Dict[str, Any]:
        """Get a collection from the database."""
        db = self._read_db()
        return db.get(collection_name, {})

    def update_collection(self, collection_name: str, data: Dict[str, Any]) -> None:
        """Update a collection in the database."""
        with self.lock:
            db = self._read_db()
            db[collection_name] = data
            self._write_db(db)

    def get_version_history(self) -> List[Dict[str, Any]]:
        """Get the version history from the database."""
        return self._read_db().get("version_history", [])

    def add_version_history_entry(
        self, version: str, revision: int, operation: str
    ) -> None:
        """Add an entry to the version history."""
        with self.lock:
            db = self._read_db()
            db["version_history"].append(
                {
                    "version": version,
                    "revision": revision,
                    "operation": operation,
                    "timestamp": datetime.now().isoformat(),
                }
            )
            self._write_db(db)

    def update_software_version(
        self, version: str, revision: int, operation: str = "upgrade"
    ) -> None:
        """Update the software version in the system info and add a history entry."""
        with self.lock:
            db = self._read_db()
            # Update system info
            db["system"]["softwareVersion"] = version
            db["system"][
                "softwareFullVersion"
            ] = f"Unity {version} (Release, Build {revision})"
            # Add history entry
            db["version_history"].append(
                {
                    "version": version,
                    "revision": revision,
                    "operation": operation,
                    "timestamp": datetime.now().isoformat(),
                }
            )
            self._write_db(db)

    def get_system_info(self) -> Dict[str, Any]:
        """Get the system information from the database."""
        return self._read_db().get("system", {})

    def update_system_info(self, system_info: Dict[str, Any]) -> None:
        """Update the system information in the database."""
        with self.lock:
            db = self._read_db()
            db["system"] = system_info
            self._write_db(db)


# Initialize the database instance
db = Storage("data/system_state.json")

# Create property-like interfaces for collections
sessions = db.get_collection("sessions")
users = db.get_collection("users")
candidate_software_versions = db.get_collection("candidate_software_versions")
upgrade_sessions = db.get_collection("upgrade_sessions")
uploaded_files = db.get_collection("uploaded_files")
installed_software_versions = db.get_collection("installed_software_versions")

# Expose necessary functions at module level
get_system_info = db.get_system_info
update_system_info = db.update_system_info
get_version_history = db.get_version_history
add_version_history_entry = db.add_version_history_entry
update_software_version = db.update_software_version
