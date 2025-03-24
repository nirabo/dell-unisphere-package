#!/usr/bin/env python3
"""Utility script to view the current state of the JSON database."""

import json

# Import the database module
from dell_unisphere_package.utils.db import DEFAULT_DB_PATH

# Add the project root to the Python path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def view_db():
    """View the current state of the JSON database."""
    if not DEFAULT_DB_PATH.exists():
        print(f"Database file not found at {DEFAULT_DB_PATH}")
        return

    try:
        with open(DEFAULT_DB_PATH, "r") as f:
            data = json.load(f)

        # Print the database in a formatted way
        print(json.dumps(data, indent=2))

        # Print some useful information
        print("\n=== Database Summary ===")
        print(f"Database path: {DEFAULT_DB_PATH}")
        print(f"System version: {data.get('system', {}).get('softwareVersion', 'N/A')}")
        print(
            f"System full version: {data.get('system', {}).get('softwareFullVersion', 'N/A')}"
        )
        print(f"Number of users: {len(data.get('users', {}))}")
        print(f"Number of sessions: {len(data.get('sessions', {}))}")
        print(f"Number of upgrade sessions: {len(data.get('upgrade_sessions', {}))}")
        print(
            f"Number of candidate software versions: {len(data.get('candidate_software_versions', {}))}"
        )
        print(
            f"Number of installed software versions: {len(data.get('installed_software_versions', {}))}"
        )
        print(
            f"Number of version history entries: {len(data.get('version_history', []))}"
        )

        # Print version history
        print("\n=== Version History ===")
        for entry in data.get("version_history", []):
            print(
                f"{entry.get('timestamp', 'N/A')} - {entry.get('operation', 'N/A')} to "
                f"{entry.get('version', 'N/A')} (revision {entry.get('revision', 'N/A')})"
            )

    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading database: {e}")


if __name__ == "__main__":
    view_db()
