"""JSON file-based database for Dell Unisphere Mock API.

This module provides functionality for storing and retrieving system state
in a JSON file, ensuring persistence across restarts and proper state management
during operations like upgrades and downgrades.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Default path for the database file
DEFAULT_DB_PATH = Path("data/system_state.json")

# Ensure the data directory exists
DEFAULT_DB_PATH.parent.mkdir(parents=True, exist_ok=True)


class JsonDatabase:
    """JSON file-based database for system state management."""

    def __init__(self, db_path: Optional[Path] = None):
        """Initialize the database with the given path.

        Args:
            db_path: Path to the JSON database file. If None, uses the default path.
        """
        self.db_path = db_path or DEFAULT_DB_PATH
        self._data = None
        self._initialize_db()

    def _initialize_db(self) -> None:
        """Initialize the database if it doesn't exist."""
        if not self.db_path.exists():
            logger.info(f"Creating new database at {self.db_path}")
            # Create initial state
            initial_state = {
                "system": {
                    "id": "0",
                    "model": "Unity 380F",
                    "name": "CKM01204905476",
                    "softwareVersion": "5.3.0",
                    "softwareFullVersion": (
                        "Unity 5.3.0.0 (Release, Build 120, 2023-03-18 19:02:01, 5.3.0.0.5.120)"
                    ),
                    "apiVersion": "13.0",
                    "earliestApiVersion": "4.0",
                },
                "users": {
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
                },
                "sessions": {},
                "candidate_software_versions": {},
                "upgrade_sessions": {},
                "uploaded_files": {},
                "installed_software_versions": {
                    "0": {
                        "id": "0",
                        "version": "5.3.0",
                        "revision": 120,
                        "releaseDate": datetime.now().isoformat(),
                        "fullVersion": (
                            "Unity 5.3.0.0 (Release, Build 120, 2023-03-18 19:02:01, 5.3.0.0.5.120)"
                        ),
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
                },
                "version_history": [
                    {
                        "version": "5.3.0",
                        "revision": 120,
                        "timestamp": datetime.now().isoformat(),
                        "operation": "initial",
                    }
                ],
            }
            self._data = initial_state
            self._save_db()
        else:
            self._load_db()

    def _load_db(self) -> None:
        """Load the database from the JSON file."""
        try:
            with open(self.db_path, "r") as f:
                self._data = json.load(f)
            logger.info(f"Loaded database from {self.db_path}")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"Error loading database: {e}")
            # Create a new database if there's an error
            self._data = {}
            self._initialize_db()

    def _save_db(self) -> None:
        """Save the database to the JSON file."""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

            with open(self.db_path, "w") as f:
                json.dump(self._data, f, indent=2)
            logger.info(f"Saved database to {self.db_path}")
        except Exception as e:
            logger.error(f"Error saving database: {e}")

    def get_collection(self, collection_name: str) -> Dict[str, Any]:
        """Get a collection from the database.

        Args:
            collection_name: Name of the collection to retrieve.

        Returns:
            The collection as a dictionary.
        """
        if collection_name not in self._data:
            self._data[collection_name] = {}
            self._save_db()
        return self._data[collection_name]

    def update_collection(self, collection_name: str, data: Dict[str, Any]) -> None:
        """Update a collection in the database.

        Args:
            collection_name: Name of the collection to update.
            data: New data for the collection.
        """
        self._data[collection_name] = data
        self._save_db()

    def get_item(self, collection_name: str, item_id: str) -> Optional[Dict[str, Any]]:
        """Get an item from a collection.

        Args:
            collection_name: Name of the collection.
            item_id: ID of the item to retrieve.

        Returns:
            The item as a dictionary, or None if not found.
        """
        collection = self.get_collection(collection_name)
        return collection.get(item_id)

    def add_item(
        self, collection_name: str, item_id: str, data: Dict[str, Any]
    ) -> None:
        """Add an item to a collection.

        Args:
            collection_name: Name of the collection.
            item_id: ID of the item to add.
            data: Data for the item.
        """
        collection = self.get_collection(collection_name)
        collection[item_id] = data
        self.update_collection(collection_name, collection)

    def update_item(
        self, collection_name: str, item_id: str, data: Dict[str, Any]
    ) -> None:
        """Update an item in a collection.

        Args:
            collection_name: Name of the collection.
            item_id: ID of the item to update.
            data: New data for the item.
        """
        collection = self.get_collection(collection_name)
        if item_id in collection:
            collection[item_id] = data
            self.update_collection(collection_name, collection)

    def delete_item(self, collection_name: str, item_id: str) -> None:
        """Delete an item from a collection.

        Args:
            collection_name: Name of the collection.
            item_id: ID of the item to delete.
        """
        collection = self.get_collection(collection_name)
        if item_id in collection:
            del collection[item_id]
            self.update_collection(collection_name, collection)

    def get_system_info(self) -> Dict[str, Any]:
        """Get the system information.

        Returns:
            The system information as a dictionary.
        """
        return self._data.get("system", {})

    def update_system_info(self, system_info: Dict[str, Any]) -> None:
        """Update the system information.

        Args:
            system_info: New system information.
        """
        self._data["system"] = system_info
        self._save_db()

    def get_version_history(self) -> list:
        """Get the version history.

        Returns:
            The version history as a list.
        """
        return self._data.get("version_history", [])

    def add_version_history_entry(
        self, version: str, revision: int, operation: str
    ) -> None:
        """Add an entry to the version history.

        Args:
            version: The software version.
            revision: The revision number.
            operation: The operation (upgrade, downgrade, etc.).
        """
        history = self.get_version_history()
        entry = {
            "version": version,
            "revision": revision,
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
        }
        history.append(entry)
        self._data["version_history"] = history
        self._save_db()

    def update_software_version(
        self, version: str, revision: int, operation: str = "upgrade"
    ) -> None:
        """Update the software version in the system info and add a history entry.

        Args:
            version: The new software version.
            revision: The new revision number.
            operation: The operation (upgrade, downgrade, etc.).
        """
        # Update system info
        system_info = self.get_system_info()
        system_info["softwareVersion"] = version
        system_info["softwareFullVersion"] = (
            f"Unity {version}.0 (Release, Build {revision}, "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, "
            f"{version}.0.5.{revision})"
        )
        self.update_system_info(system_info)

        # Update installed software version
        installed_versions = self.get_collection("installed_software_versions")
        if "0" in installed_versions:
            installed_version = installed_versions["0"]
            installed_version["version"] = version
            installed_version["revision"] = revision
            installed_version["fullVersion"] = system_info["softwareFullVersion"]
            installed_version["releaseDate"] = datetime.now().isoformat()

            # Update package versions
            for package in installed_version["packageVersions"]:
                package["version"] = version

            # Update language versions
            for language in installed_version["languages"]:
                language["version"] = version

            self.update_item("installed_software_versions", "0", installed_version)

        # Add history entry
        self.add_version_history_entry(version, revision, operation)


# Create a singleton instance
db = JsonDatabase()
