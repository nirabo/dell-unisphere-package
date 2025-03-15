#!/usr/bin/env python3
"""
Dell Unisphere Upgrade Monitor Example

This script demonstrates how to monitor an upgrade session using the Dell Unisphere API.
It shows how to:
1. Authenticate with the API
2. Create an upgrade session
3. Monitor the progress of the upgrade
4. Handle pause and resume operations

Usage:
    python upgrade_monitor.py

Requirements:
    - requests
    - rich (for pretty printing)
"""

import argparse
import sys
from datetime import datetime

import requests
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn
from rich.table import Table

# Configuration
API_BASE_URL = "http://localhost:8000"  # Update with your API URL
USERNAME = "admin"
PASSWORD = "Password123!"
POLL_INTERVAL = 5  # seconds


def login():
    """Authenticate with the API and return the session."""
    session = requests.Session()
    response = session.post(
        f"{API_BASE_URL}/api/instances/authService/action/login",
        json={"username": USERNAME, "password": PASSWORD},
    )

    if response.status_code != 200:
        print(f"Authentication failed: {response.text}")
        sys.exit(1)

    # Get CSRF token from cookies if available
    csrf_token = session.cookies.get("csrftoken")
    if csrf_token:
        session.headers.update({"X-CSRFToken": csrf_token})

    return session


def get_candidate_versions(session):
    """Get available candidate software versions."""
    response = session.get(
        f"{API_BASE_URL}/api/types/candidateSoftwareVersion/instances"
    )

    if response.status_code != 200:
        print(f"Failed to get candidate versions: {response.text}")
        return []

    data = response.json()
    return data.get("content", [])


def create_upgrade_session(session, candidate_id):
    """Create a new upgrade session."""
    response = session.post(
        f"{API_BASE_URL}/api/types/upgradeSession/instances",
        json={"candidate": candidate_id},
    )

    if response.status_code != 200:
        print(f"Failed to create upgrade session: {response.text}")
        return None

    return response.json().get("id")


def get_upgrade_session(session, session_id):
    """Get the current state of an upgrade session."""
    response = session.get(
        f"{API_BASE_URL}/api/types/upgradeSession/instances?fields=id,status,caption,percentComplete,tasks,messages",
    )

    if response.status_code != 200:
        print(f"Failed to get upgrade session: {response.text}")
        return None

    data = response.json()
    sessions = data.get("content", [])

    # Find the session with the matching ID
    for s in sessions:
        if s.get("id") == session_id:
            return s

    return None


def pause_upgrade(session, session_id):
    """Pause an in-progress upgrade."""
    response = session.post(
        f"{API_BASE_URL}/api/instances/upgradeSession/{session_id}/action/pause",
    )

    if response.status_code != 200:
        print(f"Failed to pause upgrade: {response.text}")
        return False

    return True


def resume_upgrade(session, session_id):
    """Resume a paused upgrade."""
    response = session.post(
        f"{API_BASE_URL}/api/instances/upgradeSession/{session_id}/action/resume",
    )

    if response.status_code != 200:
        print(f"Failed to resume upgrade: {response.text}")
        return False

    return True


def display_upgrade_status(upgrade_session):
    """Display the current status of the upgrade session."""
    console = Console()

    # Clear the console
    console.clear()

    if not upgrade_session:
        console.print("[bold red]No upgrade session data available[/bold red]")
        return

    # Display session info
    session_id = upgrade_session.get("id", "Unknown")
    status = upgrade_session.get("status", 0)
    percent_complete = upgrade_session.get("percentComplete", 0)
    caption = upgrade_session.get("caption", "Unknown")

    status_map = {
        0: "[yellow]PENDING[/yellow]",
        1: "[blue]IN_PROGRESS[/blue]",
        2: "[green]COMPLETED[/green]",
        3: "[red]FAILED[/red]",
        4: "[magenta]PAUSED[/magenta]",
    }

    status_text = status_map.get(status, f"[gray]UNKNOWN ({status})[/gray]")

    # Create session info panel
    session_info = f"""
    [bold]Session ID:[/bold] {session_id}
    [bold]Caption:[/bold] {caption}
    [bold]Status:[/bold] {status_text}
    [bold]Progress:[/bold] {percent_complete}%
    """

    console.print(Panel(session_info, title="Upgrade Session", expand=False))

    # Display progress bar
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
        expand=True,
    ) as progress:
        task = progress.add_task(
            "[cyan]Overall Progress", total=100, completed=percent_complete
        )
        progress.update(task, completed=percent_complete, refresh=True)

    # Display tasks
    tasks = upgrade_session.get("tasks", [])

    task_status_map = {
        0: "⏳ PENDING",
        1: "🔄 IN_PROGRESS",
        2: "✅ COMPLETED",
        3: "❌ FAILED",
        4: "⏸️ PAUSED",
    }

    table = Table(title="Upgrade Tasks")
    table.add_column("Task", style="cyan")
    table.add_column("Status", style="magenta")
    table.add_column("Est. Time", style="green")

    for task in tasks:
        caption = task.get("caption", "Unknown")
        status = task.get("status", 0)
        est_time = task.get("estRemainTime", "Unknown")

        status_text = task_status_map.get(status, f"UNKNOWN ({status})")

        table.add_row(caption, status_text, est_time)

    console.print(table)

    # Display messages
    messages = upgrade_session.get("messages", [])

    if messages:
        message_table = Table(title="Messages")
        message_table.add_column("Time", style="cyan")
        message_table.add_column("Message", style="white")

        for message in messages:
            timestamp = message.get("timestamp", "")
            msg_text = message.get("message", "")

            # Format timestamp
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                    timestamp = dt.strftime("%H:%M:%S")
                except ValueError:
                    pass

            message_table.add_row(timestamp, msg_text)

        console.print(message_table)

    # Display commands
    commands_text = """
    Commands:
    p - Pause upgrade
    r - Resume upgrade
    q - Quit
    """

    console.print(Panel(commands_text, title="Available Commands", expand=False))


def monitor_upgrade(session, session_id):
    """Monitor the progress of an upgrade session."""
    console = Console()

    try:
        while True:
            # Get the current state of the upgrade session
            upgrade_session = get_upgrade_session(session, session_id)

            # Display the current status
            display_upgrade_status(upgrade_session)

            # Check if the upgrade is complete or failed
            status = upgrade_session.get("status", 0)
            if status == 2:  # COMPLETED
                console.print(
                    "[bold green]Upgrade completed successfully![/bold green]"
                )
                break
            elif status == 3:  # FAILED
                console.print("[bold red]Upgrade failed![/bold red]")
                break

            # Wait for user input with timeout
            console.print(
                (
                    f"\nPolling for updates every {POLL_INTERVAL} seconds."
                    "Press a command key or Enter to refresh immediately..."
                )
            )

            # Non-blocking input with timeout
            import select
            import sys

            # Wait for input or timeout
            ready, _, _ = select.select([sys.stdin], [], [], POLL_INTERVAL)

            if ready:
                command = sys.stdin.readline().strip().lower()

                if command == "p":
                    if status == 1:  # IN_PROGRESS
                        console.print("[yellow]Pausing upgrade...[/yellow]")
                        pause_upgrade(session, session_id)
                    else:
                        console.print(
                            "[yellow]Upgrade is not in progress, cannot pause.[/yellow]"
                        )

                elif command == "r":
                    if status == 4:  # PAUSED
                        console.print("[yellow]Resuming upgrade...[/yellow]")
                        resume_upgrade(session, session_id)
                    else:
                        console.print(
                            "[yellow]Upgrade is not paused, cannot resume.[/yellow]"
                        )

                elif command == "q":
                    console.print("[yellow]Exiting...[/yellow]")
                    break

    except KeyboardInterrupt:
        console.print("[yellow]Monitoring interrupted. Exiting...[/yellow]")


def main():
    """Main function to run the upgrade monitor."""
    console = Console()

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Dell Unisphere Upgrade Monitor")
    parser.add_argument("--session-id", help="Existing upgrade session ID to monitor")
    parser.add_argument(
        "--candidate", help="Candidate software version ID to upgrade to"
    )
    args = parser.parse_args()

    # Authenticate with the API
    console.print("[yellow]Authenticating with the API...[/yellow]")
    session = login()
    console.print("[green]Authentication successful![/green]")

    session_id = args.session_id

    if not session_id:
        # Get candidate versions
        console.print("[yellow]Getting candidate software versions...[/yellow]")
        candidates = get_candidate_versions(session)

        if not candidates:
            console.print(
                "[bold red]No candidate software versions available.[/bold red]"
            )
            return

        # Display available candidates
        table = Table(title="Available Candidate Software Versions")
        table.add_column("ID", style="cyan")
        table.add_column("Version", style="green")
        table.add_column("Full Version", style="blue")

        for candidate in candidates:
            table.add_row(
                candidate.get("id", "Unknown"),
                candidate.get("version", "Unknown"),
                candidate.get("fullVersion", "Unknown"),
            )

        console.print(table)

        # Select candidate
        candidate_id = args.candidate

        if not candidate_id:
            if len(candidates) == 1:
                candidate_id = candidates[0].get("id")
                console.print(
                    f"[yellow]Using the only available candidate: {candidate_id}[/yellow]"
                )
            else:
                console.print(
                    "[yellow]Please select a candidate ID from the list above.[/yellow]"
                )
                candidate_id = input("Candidate ID: ")

        # Create upgrade session
        console.print(
            f"[yellow]Creating upgrade session for candidate {candidate_id}...[/yellow]"
        )
        session_id = create_upgrade_session(session, candidate_id)

        if not session_id:
            console.print("[bold red]Failed to create upgrade session.[/bold red]")
            return

        console.print(f"[green]Upgrade session created: {session_id}[/green]")

    # Monitor the upgrade
    console.print(f"[yellow]Monitoring upgrade session {session_id}...[/yellow]")
    monitor_upgrade(session, session_id)


if __name__ == "__main__":
    main()
