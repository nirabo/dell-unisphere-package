"""State persistence utilities for Dell Unisphere API.

This module provides utilities for persisting state to disk and loading it on server restart.
"""

import json
import logging
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

# Set up logger
logger = logging.getLogger(__name__)

# Define the state file path
STATE_DIR = Path("/tmp/dell_unisphere_state")
UPGRADE_SESSIONS_FILE = STATE_DIR / "upgrade_sessions.json"
BACKUP_FILE = STATE_DIR / "upgrade_sessions.backup.json"
CANDIDATE_SOFTWARE_FILE = STATE_DIR / "candidate_software.json"
CANDIDATE_BACKUP_FILE = STATE_DIR / "candidate_software.backup.json"


def _ensure_state_dir():
    """Ensure the state directory exists."""
    STATE_DIR.mkdir(exist_ok=True, parents=True)


def _make_json_serializable(obj):
    """Convert an object to a JSON serializable format.

    Args:
        obj: The object to convert

    Returns:
        A JSON serializable version of the object
    """
    if isinstance(obj, dict):
        return {k: _make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_make_json_serializable(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    # Handle Enum values - check for _value_ and _name_ attributes which are common in Enum classes
    elif hasattr(obj, "_value_") and hasattr(obj, "_name_"):
        # Just store the value of the enum
        return obj._value_
    elif hasattr(obj, "__dict__"):
        # Handle objects with __dict__ attribute (like Pydantic models)
        return _make_json_serializable(obj.__dict__)
    else:
        # Try to convert to a basic type, or return as is if that's not possible
        try:
            json.dumps(obj)
            return obj
        except (TypeError, OverflowError):
            # For objects that can't be serialized, just return their string representation
            # but strip out memory addresses and other non-essential information
            return str(obj).split(" at ")[0] + ">"


def save_state(
    upgrade_sessions: Dict[str, Any], candidate_software_versions: Dict[str, Any]
):
    """Save all state to disk using atomic file operations.

    Args:
        upgrade_sessions: The upgrade sessions to save
        candidate_software_versions: The candidate software versions to save
    """
    _ensure_state_dir()

    # Save upgrade sessions
    save_upgrade_sessions(upgrade_sessions)

    # Save candidate software versions
    save_candidate_software(candidate_software_versions)


def save_upgrade_sessions(upgrade_sessions: Dict[str, Any]):
    """Save upgrade sessions to disk using atomic file operations.

    Args:
        upgrade_sessions: The upgrade sessions to save
    """
    _ensure_state_dir()

    # Make a backup of the existing file if it exists
    if UPGRADE_SESSIONS_FILE.exists():
        try:
            UPGRADE_SESSIONS_FILE.rename(BACKUP_FILE)
        except Exception as e:
            logger.warning(f"Failed to create backup file: {e}")

    # Convert complex objects to JSON serializable format
    serializable_sessions = _make_json_serializable(upgrade_sessions)

    # Use atomic file operations to prevent corruption
    try:
        # Create a temporary file in the same directory
        fd, temp_path = tempfile.mkstemp(
            dir=str(STATE_DIR), prefix="upgrade_sessions_", suffix=".json.tmp"
        )

        # Write to the temporary file
        with os.fdopen(fd, "w") as temp_file:
            json.dump(serializable_sessions, temp_file, indent=2)

        # Atomically replace the target file with the temporary file
        # This ensures the file is either completely written or not at all
        os.replace(temp_path, str(UPGRADE_SESSIONS_FILE))

        logger.info(
            f"Saved {len(upgrade_sessions)} upgrade sessions to {UPGRADE_SESSIONS_FILE}"
        )

        # Remove the backup file if everything went well
        if BACKUP_FILE.exists():
            BACKUP_FILE.unlink()

    except Exception as e:
        logger.error(f"Failed to save upgrade sessions: {e}")

        # Try to restore from backup if available
        if BACKUP_FILE.exists():
            try:
                BACKUP_FILE.rename(UPGRADE_SESSIONS_FILE)
                logger.info("Restored upgrade sessions from backup file")
            except Exception as restore_error:
                logger.error(f"Failed to restore from backup: {restore_error}")


def save_candidate_software(candidate_software_versions: Dict[str, Any]):
    """Save candidate software versions to disk using atomic file operations.

    Args:
        candidate_software_versions: The candidate software versions to save
    """
    _ensure_state_dir()

    # Make a backup of the existing file if it exists
    if CANDIDATE_SOFTWARE_FILE.exists():
        try:
            CANDIDATE_SOFTWARE_FILE.rename(CANDIDATE_BACKUP_FILE)
        except Exception as e:
            logger.warning(f"Failed to create candidate backup file: {e}")

    # Convert complex objects to JSON serializable format
    serializable_candidates = _make_json_serializable(candidate_software_versions)

    # Use atomic file operations to prevent corruption
    try:
        # Create a temporary file in the same directory
        fd, temp_path = tempfile.mkstemp(
            dir=str(STATE_DIR), prefix="candidate_software_", suffix=".json.tmp"
        )

        # Write to the temporary file
        with os.fdopen(fd, "w") as temp_file:
            json.dump(serializable_candidates, temp_file, indent=2)

        # Atomically replace the target file with the temporary file
        # This ensures the file is either completely written or not at all
        os.replace(temp_path, str(CANDIDATE_SOFTWARE_FILE))

        logger.info(
            f"Saved {len(candidate_software_versions)} candidate software versions to {CANDIDATE_SOFTWARE_FILE}"
        )

        # Remove the backup file if everything went well
        if CANDIDATE_BACKUP_FILE.exists():
            CANDIDATE_BACKUP_FILE.unlink()

    except Exception as e:
        logger.error(f"Failed to save candidate software versions: {e}")

        # Try to restore from backup if available
        if CANDIDATE_BACKUP_FILE.exists():
            try:
                CANDIDATE_BACKUP_FILE.rename(CANDIDATE_SOFTWARE_FILE)
                logger.info("Restored candidate software versions from backup file")
            except Exception as restore_error:
                logger.error(f"Failed to restore from backup: {restore_error}")


def _convert_enum_values(data):
    """Convert enum values from the loaded JSON back to their proper types.

    This function handles the conversion of enum values in the loaded data.
    It looks for specific patterns in the data structure that indicate enum values.

    Args:
        data: The data loaded from JSON

    Returns:
        The data with enum values converted to their proper types
    """
    from ..schemas.base import (
        TaskStatusEnum,
        TaskTypeEnum,
        UpgradeSessionTypeEnum,
        UpgradeStatusEnum,
        UpgradeTypeEnum,
    )

    # Map of enum classes by name
    enum_classes = {
        "TaskStatusEnum": TaskStatusEnum,
        "TaskTypeEnum": TaskTypeEnum,
        "UpgradeStatusEnum": UpgradeStatusEnum,
        "UpgradeSessionTypeEnum": UpgradeSessionTypeEnum,
        "UpgradeTypeEnum": UpgradeTypeEnum,
    }

    if isinstance(data, dict):
        # Check if this dict looks like an enum value
        if "_value_" in data and "_name_" in data:
            # Try to convert it to an enum value
            for enum_name, enum_class in enum_classes.items():
                if enum_name in str(data.get("__objclass__", "")):
                    try:
                        # Convert the value to the enum
                        return enum_class(data["_value_"])
                    except (ValueError, KeyError):
                        # If conversion fails, just return the value
                        return data["_value_"]
            # If we couldn't determine the enum class, just return the value
            return data["_value_"]

        # Process each item in the dictionary
        return {k: _convert_enum_values(v) for k, v in data.items()}
    elif isinstance(data, list):
        # Process each item in the list
        return [_convert_enum_values(item) for item in data]
    else:
        # Return other values as is
        return data


def load_state():
    """Load all state from disk.

    Returns:
        A tuple containing (upgrade_sessions, candidate_software_versions)
    """
    upgrade_sessions = load_upgrade_sessions()
    candidate_software_versions = load_candidate_software()

    return upgrade_sessions, candidate_software_versions


def load_upgrade_sessions() -> Dict[str, Any]:
    """Load upgrade sessions from disk with fallback to backup file.

    Returns:
        The loaded upgrade sessions, or an empty dict if no valid file exists
    """
    # Try to load from the main file first
    if UPGRADE_SESSIONS_FILE.exists():
        try:
            with open(UPGRADE_SESSIONS_FILE, "r") as f:
                sessions = json.load(f)

            # Convert enum values in the loaded data
            sessions = _convert_enum_values(sessions)

            logger.info(
                f"Loaded {len(sessions)} upgrade sessions from {UPGRADE_SESSIONS_FILE}"
            )
            return sessions
        except Exception as e:
            logger.error(f"Failed to load upgrade sessions: {e}")

            # Try to load from backup file if main file is corrupted
            if BACKUP_FILE.exists():
                logger.info("Attempting to load from backup file")
                try:
                    with open(BACKUP_FILE, "r") as f:
                        sessions = json.load(f)

                    # Convert enum values in the loaded data
                    sessions = _convert_enum_values(sessions)

                    logger.info(
                        f"Loaded {len(sessions)} upgrade sessions from backup file"
                    )

                    # Restore the backup file as the main file
                    BACKUP_FILE.rename(UPGRADE_SESSIONS_FILE)
                    logger.info("Restored backup file as main file")

                    return sessions
                except Exception as backup_error:
                    logger.error(f"Failed to load from backup file: {backup_error}")
    elif BACKUP_FILE.exists():
        # Main file doesn't exist but backup does
        logger.info("Main file not found, attempting to load from backup file")
        try:
            with open(BACKUP_FILE, "r") as f:
                sessions = json.load(f)

            # Convert enum values in the loaded data
            sessions = _convert_enum_values(sessions)

            logger.info(f"Loaded {len(sessions)} upgrade sessions from backup file")

            # Restore the backup file as the main file
            BACKUP_FILE.rename(UPGRADE_SESSIONS_FILE)
            logger.info("Restored backup file as main file")

            return sessions
        except Exception as backup_error:
            logger.error(f"Failed to load from backup file: {backup_error}")
    else:
        logger.info(f"No upgrade sessions file found at {UPGRADE_SESSIONS_FILE}")

    return {}


def load_candidate_software() -> Dict[str, Any]:
    """Load candidate software versions from disk with fallback to backup file.

    Returns:
        The loaded candidate software versions, or an empty dict if no valid file exists
    """
    # Try to load from the main file first
    if CANDIDATE_SOFTWARE_FILE.exists():
        try:
            with open(CANDIDATE_SOFTWARE_FILE, "r") as f:
                candidates = json.load(f)

            # Convert enum values in the loaded data
            candidates = _convert_enum_values(candidates)

            logger.info(
                f"Loaded {len(candidates)} candidate software versions from {CANDIDATE_SOFTWARE_FILE}"
            )
            return candidates
        except Exception as e:
            logger.error(f"Failed to load candidate software versions: {e}")

            # Try to load from backup file if main file is corrupted
            if CANDIDATE_BACKUP_FILE.exists():
                logger.info("Attempting to load from candidate backup file")
                try:
                    with open(CANDIDATE_BACKUP_FILE, "r") as f:
                        candidates = json.load(f)

                    # Convert enum values in the loaded data
                    candidates = _convert_enum_values(candidates)

                    logger.info(
                        f"Loaded {len(candidates)} candidate software versions from backup file"
                    )

                    # Restore the backup file as the main file
                    CANDIDATE_BACKUP_FILE.rename(CANDIDATE_SOFTWARE_FILE)
                    logger.info("Restored candidate backup file as main file")

                    return candidates
                except Exception as backup_error:
                    logger.error(
                        f"Failed to load from candidate backup file: {backup_error}"
                    )
    elif CANDIDATE_BACKUP_FILE.exists():
        # Main file doesn't exist but backup does
        logger.info(
            "Main candidate file not found, attempting to load from backup file"
        )
        try:
            with open(CANDIDATE_BACKUP_FILE, "r") as f:
                candidates = json.load(f)

            # Convert enum values in the loaded data
            candidates = _convert_enum_values(candidates)

            logger.info(
                f"Loaded {len(candidates)} candidate software versions from backup file"
            )

            # Restore the backup file as the main file
            CANDIDATE_BACKUP_FILE.rename(CANDIDATE_SOFTWARE_FILE)
            logger.info("Restored candidate backup file as main file")

            return candidates
        except Exception as backup_error:
            logger.error(f"Failed to load from candidate backup file: {backup_error}")
    else:
        logger.info(
            f"No candidate software versions file found at {CANDIDATE_SOFTWARE_FILE}"
        )

    return {}
