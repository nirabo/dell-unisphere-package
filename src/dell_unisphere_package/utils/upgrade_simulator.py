"""Upgrade simulation utilities for Dell Unisphere API.

This module provides utilities for simulating software upgrade processes.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List

from ..models.storage import candidate_software_versions, upgrade_sessions
from ..schemas.base import TaskStatusEnum, TaskTypeEnum, UpgradeStatusEnum

# Set up logger
logger = logging.getLogger(__name__)

# Configuration for time acceleration
# For reboot task, we want it to last approximately 60 seconds
SIMULATION_SPEED_FACTOR = 40  # Slowed down to better observe the reboot behavior

# Store active simulation tasks
active_simulations = {}
active_tasks = {}


def parse_time_to_seconds(time_str: str) -> int:
    """Parse a time string in format HH:MM:SS.mmm to seconds."""
    hours, minutes, seconds = time_str.split(":")
    seconds = seconds.split(".")[0]  # Remove milliseconds
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds)


def format_timedelta(td: timedelta) -> str:
    """Format a timedelta to ISO 8601 duration format."""
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"PT{hours}H{minutes}M{seconds}S"


def create_realistic_upgrade_tasks() -> List[Dict[str, Any]]:
    """Create a realistic list of upgrade tasks with proper timing."""
    now = datetime.now()

    return [
        {
            "status": TaskStatusEnum.PENDING,
            "type": TaskTypeEnum.PREPARE,
            "caption": "Preparing system",
            "creationTime": now.isoformat(),
            "estRemainTime": "00:03:30.000",
        },
        {
            "status": TaskStatusEnum.PENDING,
            "type": TaskTypeEnum.PREPARE,
            "caption": "Performing health checks",
            "creationTime": now.isoformat(),
            "estRemainTime": "00:02:10.000",
        },
        {
            "status": TaskStatusEnum.PENDING,
            "type": TaskTypeEnum.PREPARE,
            "caption": "Preparing system software",
            "creationTime": now.isoformat(),
            "estRemainTime": "00:16:10.000",
        },
        {
            "status": TaskStatusEnum.PENDING,
            "type": TaskTypeEnum.PREPARE,
            "caption": "Waiting for reboot command",
            "creationTime": now.isoformat(),
            "estRemainTime": "00:00:05.000",
        },
        {
            "status": TaskStatusEnum.PENDING,
            "type": TaskTypeEnum.PREPARE,
            "caption": "Performing health checks",
            "creationTime": now.isoformat(),
            "estRemainTime": "00:01:05.000",
        },
        {
            "status": TaskStatusEnum.PENDING,
            "type": TaskTypeEnum.INSTALL,
            "caption": "Installing new software on peer SP",
            "creationTime": now.isoformat(),
            "estRemainTime": "00:16:50.000",
        },
        {
            "status": TaskStatusEnum.PENDING,
            "type": TaskTypeEnum.REBOOT,
            "caption": "Rebooting peer SP",
            "creationTime": now.isoformat(),
            "estRemainTime": "00:14:15.000",
        },
        {
            "status": TaskStatusEnum.PENDING,
            "type": TaskTypeEnum.INSTALL,
            "caption": "Restarting services on peer SP",
            "creationTime": now.isoformat(),
            "estRemainTime": "00:05:00.000",
        },
        {
            "status": TaskStatusEnum.PENDING,
            "type": TaskTypeEnum.INSTALL,
            "caption": "Installing new software on primary SP",
            "creationTime": now.isoformat(),
            "estRemainTime": "00:13:30.000",
        },
        {
            "status": TaskStatusEnum.PENDING,
            "type": TaskTypeEnum.REBOOT,
            "caption": "Rebooting the primary SP",
            "creationTime": now.isoformat(),
            "estRemainTime": "00:13:55.000",
        },
        {
            "status": TaskStatusEnum.PENDING,
            "type": TaskTypeEnum.INSTALL,
            "caption": "Restarting services on primary SP",
            "creationTime": now.isoformat(),
            "estRemainTime": "00:05:10.000",
        },
        {
            "status": TaskStatusEnum.PENDING,
            "type": TaskTypeEnum.INSTALL,
            "caption": "Final tasks",
            "creationTime": now.isoformat(),
            "estRemainTime": "00:00:45.000",
        },
    ]


async def simulate_task_execution(task_duration, session_id, task_index, total_tasks):
    """Simulate the execution of a single task.

    Args:
        task_duration: Duration of the task in seconds
        session_id: ID of the upgrade session
        task_index: Index of the task in the session's tasks list
        total_tasks: Total number of tasks in the session
    """
    if session_id not in upgrade_sessions:
        logger.error(f"Session {session_id} not found during task execution")
        return False

    session = upgrade_sessions[session_id]

    # Check if task index is valid
    if task_index >= len(session["tasks"]):
        logger.error(
            f"Task index {task_index} is out of range for session {session_id}"
        )
        return False

    task = session["tasks"][task_index]

    # Set task to IN_PROGRESS immediately
    task["status"] = TaskStatusEnum.IN_PROGRESS

    # Add a message about starting the task
    session["messages"].append(
        {
            "timestamp": datetime.now().isoformat(),
            "message": f"Starting task: {task['caption']}",
            "severity": 0,
        }
    )

    # Simulate task execution with progress updates
    increment_count = 10  # Number of progress updates
    for j in range(increment_count):
        # Check if session still exists
        if session_id not in upgrade_sessions:
            logger.info(f"Session {session_id} no longer exists during task execution")
            return False

        # Refresh session reference as it might have been updated
        session = upgrade_sessions[session_id]

        # Check if task index is still valid
        if task_index >= len(session["tasks"]):
            logger.info(
                f"Task index {task_index} is now out of range for session {session_id}"
            )
            return False

        # Check if we should stop
        if session_id not in active_simulations:
            logger.info(
                f"Task {task_index+1} stopped: simulation for session {session_id} was stopped"
            )
            return False

        # Check if we should pause
        if session["status"] == UpgradeStatusEnum.PAUSED:
            logger.info(f"Task {task_index+1} paused: session {session_id} is paused")
            while session["status"] == UpgradeStatusEnum.PAUSED:
                if session_id not in active_simulations:
                    return False
                await asyncio.sleep(0.1)
            logger.info(f"Task {task_index+1} resumed: session {session_id} resumed")

        # Sleep for a fraction of the task duration
        sleep_time = task_duration / increment_count
        try:
            await asyncio.sleep(sleep_time)

            # Calculate completed tasks so far (including partial completion of current task)
            completed = task_index + (j + 1) / increment_count
            session["percentComplete"] = int((completed / total_tasks) * 100)

            logger.debug(
                f"Task {task_index+1} progress: {(j+1)/increment_count:.1f}, Overall: {session['percentComplete']}%"
            )
        except asyncio.CancelledError:
            logger.info(f"Task {task_index+1} for session {session_id} was cancelled")
            raise

    # Check if session still exists before updating task status
    if session_id not in upgrade_sessions:
        logger.info(f"Session {session_id} no longer exists, cannot update task status")
        return False

    # Refresh session reference
    session = upgrade_sessions[session_id]

    # Check if task index is still valid
    if task_index >= len(session["tasks"]):
        logger.info(
            f"Task index {task_index} is now out of range, cannot update task status"
        )
        return False

    # Get the task again as it might have been updated
    task = session["tasks"][task_index]

    # Task completed successfully
    task["status"] = TaskStatusEnum.COMPLETED

    # Add a message about task completion
    session["messages"].append(
        {
            "timestamp": datetime.now().isoformat(),
            "message": f"Completed task: {task['caption']}",
            "severity": 0,
        }
    )

    logger.info(f"Task {task_index+1} completed successfully")
    return True


async def process_upgrade_session(session_id: str):
    """Process an upgrade session in the background."""
    # Add print statement for immediate console output
    print(f"DEBUG: process_upgrade_session started for {session_id}")

    # Use both logger.info and logger.warning to see if one works
    logger.info(f"Starting upgrade simulation for session {session_id}")
    logger.warning(
        f"Starting upgrade simulation for session {session_id} (WARNING level)"
    )

    if session_id not in upgrade_sessions:
        logger.error(f"Session {session_id} not found")
        print(f"DEBUG: Session {session_id} not found")
        return

    session = upgrade_sessions[session_id]
    print(f"DEBUG: Found session {session_id} with status {session.get('status')}")

    # Initialize list to track asyncio tasks
    tasks = []

    # Check if session is paused and wait for resume
    if session["status"] == UpgradeStatusEnum.PAUSED:
        logger.info(f"Upgrade session {session_id} is paused, waiting for resume")
        while session["status"] == UpgradeStatusEnum.PAUSED:
            await asyncio.sleep(0.1)
            # If session was deleted or cancelled, exit
            if session_id not in upgrade_sessions:
                return

    # Always ensure the session is in IN_PROGRESS state
    session["status"] = UpgradeStatusEnum.IN_PROGRESS
    logger.info(f"Upgrade session {session_id} is now in progress")

    # Make sure startTime is set
    if "startTime" not in session:
        session["startTime"] = datetime.now().isoformat()

    # Initialize messages array if not present
    if "messages" not in session:
        session["messages"] = []

    # Verify candidate exists
    candidate_id = session.get("candidate")
    if not candidate_id or candidate_id not in candidate_software_versions:
        session["status"] = UpgradeStatusEnum.FAILED
        session["messages"].append(
            {
                "timestamp": datetime.now().isoformat(),
                "message": "Candidate software version not found",
                "severity": 2,
            }
        )
        # Raise an exception to signal the failure to tests
        raise Exception("Candidate software version not found")

    # Process each task in sequence
    total_tasks = len(session["tasks"])
    completed_tasks = 0

    try:
        # Process each task
        for i, task in enumerate(session["tasks"]):
            # Check if session still exists (might have been deleted or stopped)
            if session_id not in upgrade_sessions:
                logger.info(
                    f"Session {session_id} no longer exists, stopping simulation"
                )
                return

            # Get the current session state (it might have been updated)
            session = upgrade_sessions[session_id]

            # Check if session is cancelled or failed
            if session["status"] in [
                UpgradeStatusEnum.FAILED,
                UpgradeStatusEnum.CANCELLED,
            ]:
                logger.info(
                    f"Session {session_id} is in {session['status']} state, stopping simulation"
                )
                return

            # Check if tasks array has been modified and this task no longer exists
            if i >= len(session["tasks"]):
                logger.info(
                    f"Task index {i} is out of range for session {session_id}, stopping simulation"
                )
                return

            # Check if task is a dictionary or a Pydantic model
            if hasattr(task, "status"):
                # It's a Pydantic model, use attribute access
                if task.status == TaskStatusEnum.COMPLETED:
                    completed_tasks += 1
                    continue

                # Set task to IN_PROGRESS immediately
                task.status = TaskStatusEnum.IN_PROGRESS

                # Add a message about starting the task
                session["messages"].append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "message": f"Starting task: {task.caption}",
                        "severity": 0,
                    }
                )
            else:
                # It's a dictionary, use dictionary access
                if task["status"] == TaskStatusEnum.COMPLETED:
                    completed_tasks += 1
                    continue

                # Set task to IN_PROGRESS immediately
                task["status"] = TaskStatusEnum.IN_PROGRESS

                # Add a message about starting the task
                session["messages"].append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "message": f"Starting task: {task['caption']}",
                        "severity": 0,
                    }
                )

            # Update session percentage based on tasks completed so far
            session["percentComplete"] = int((completed_tasks / total_tasks) * 100)

            # Check if session is paused
            if session["status"] == UpgradeStatusEnum.PAUSED:
                logger.info(f"Upgrade session {session_id} paused during task {i+1}")
                # Wait until resumed or cancelled
                while session["status"] == UpgradeStatusEnum.PAUSED:
                    await asyncio.sleep(0.1)
                    # If session was deleted or cancelled, exit
                    if session_id not in upgrade_sessions:
                        return

            # Handle task properties based on its type
            if hasattr(task, "status"):
                # It's a Pydantic model - we need to update the session's task list directly
                # since we can't modify the Pydantic model

                # Get estimated time from the model
                if hasattr(task, "estimatedTime"):
                    est_time = task.estimatedTime
                elif hasattr(task, "estRemainTime"):
                    est_time = task.estRemainTime
                else:
                    est_time = "00:01:00.000"

                task_caption = task.caption

                # Update the task in the session's task list
                # We need to convert the Pydantic model to a dict
                if not isinstance(session["tasks"][i], dict):
                    # Convert the task to a dictionary
                    task_dict = task.model_dump()
                    # Replace the task in the session's task list
                    session["tasks"][i] = task_dict
            else:
                # It's a dictionary - no need to add startTime to match the original schema

                # Get estimated time from dictionary
                est_time = task.get(
                    "estimatedTime", task.get("estRemainTime", "00:01:00.000")
                )

                task_caption = task["caption"]

            duration = parse_time_to_seconds(est_time) / SIMULATION_SPEED_FACTOR

            logger.info(
                f"Task {i+1}/{total_tasks}: {task_caption} duration: {duration} seconds"
            )

            # Log task start
            logger.info(f"Starting task {i+1}/{total_tasks}: {task_caption}")

            # Create a task for this step
            task_obj = asyncio.create_task(
                simulate_task_execution(duration, session_id, i, total_tasks)
            )
            tasks.append(task_obj)

            # Wait for this task to complete before moving to the next one
            try:
                await task_obj

                # Mark task as completed based on its type
                if hasattr(task, "status"):
                    # It's a Pydantic model - we need to update the session's task list
                    task_caption = task.caption

                    # Update the task in the session's task list
                    if isinstance(session["tasks"][i], dict):
                        session["tasks"][i]["status"] = TaskStatusEnum.COMPLETED
                    else:
                        # Convert the task to a dictionary, update it, and replace it in the list
                        task_dict = task.model_dump()
                        task_dict["status"] = TaskStatusEnum.COMPLETED
                        session["tasks"][i] = task_dict
                else:
                    # It's a dictionary
                    task["status"] = TaskStatusEnum.COMPLETED
                    task_caption = task["caption"]

                completed_tasks += 1

                # Update session progress percentage
                session["percentComplete"] = int(completed_tasks / total_tasks * 100)

                # Add a message about task completion
                session["messages"].append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "message": f"Completed task: {task_caption}",
                        "severity": 0,
                    }
                )

                logger.info(f"Completed task {i+1}/{total_tasks}: {task_caption}")
            except asyncio.CancelledError:
                logger.info(f"Task {i+1} was cancelled")
                # Propagate the cancellation
                raise
            except Exception as e:
                logger.error(f"Error in task {i+1}: {str(e)}")
                # Mark session as failed
                session["status"] = UpgradeStatusEnum.FAILED
                raise

            # Task completion is now handled in the task execution loop above

        # All tasks have been processed
        if completed_tasks == total_tasks:
            # Set status to COMPLETED
            session["status"] = UpgradeStatusEnum.COMPLETED
            session["percentComplete"] = 100
            session["endTime"] = datetime.now().isoformat()
            session["elapsedTime"] = format_timedelta(
                datetime.now() - datetime.fromisoformat(session["startTime"])
            )

            # Remove candidate after successful upgrade
            if "candidate" in session:
                candidate_id = session["candidate"]
                if candidate_id in candidate_software_versions:
                    del candidate_software_versions[candidate_id]
                    logger.info(
                        f"Removed candidate {candidate_id} after successful upgrade"
                    )

            logger.info(f"Upgrade session {session_id} completed successfully")
    except asyncio.CancelledError:
        logger.info(f"Upgrade session {session_id} was cancelled")
        session["status"] = UpgradeStatusEnum.FAILED
        raise
    except Exception as e:
        logger.error(f"Error processing upgrade session {session_id}: {e}")
        session["status"] = UpgradeStatusEnum.FAILED
        raise
    finally:
        # Clean up active tasks but keep the session for status checking
        if session_id in active_tasks:
            del active_tasks[session_id]

    # Return the session ID for reference
    return session_id


def start_upgrade_simulation(session_id: str):
    """Start a new upgrade simulation for the given session."""
    if session_id in active_simulations:
        logger.warning(f"Simulation for session {session_id} is already running")
        return

    # Log that we're starting the simulation
    logger.info(f"Initializing upgrade simulation for session {session_id}")
    print(f"DEBUG: Initializing upgrade simulation for session {session_id}")

    # Use a completely different approach with a dedicated thread for the task
    import threading

    def run_async_task():
        print(f"DEBUG: Thread started for session {session_id}")
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Run the coroutine to completion in this thread
            print(f"DEBUG: About to run process_upgrade_session for {session_id}")
            result = loop.run_until_complete(process_upgrade_session(session_id))
            print(
                f"DEBUG: process_upgrade_session completed for {session_id} with result: {result}"
            )
            return result
        except Exception as e:
            # Check if session was intentionally stopped
            if session_id not in upgrade_sessions:
                print(
                    f"DEBUG: Session {session_id} was stopped, ignoring exception: {str(e)}"
                )
                logger.info(f"Upgrade simulation for session {session_id} was stopped")
            elif session_id in upgrade_sessions and upgrade_sessions[session_id][
                "status"
            ] in [UpgradeStatusEnum.FAILED, UpgradeStatusEnum.CANCELLED]:
                status_str = str(upgrade_sessions[session_id]["status"].value).lower()
                print(
                    f"DEBUG: Session {session_id} was already marked as {status_str}, ignoring exception: {str(e)}"
                )
                logger.info(
                    f"Upgrade simulation for session {session_id} was {status_str}"
                )
            else:
                print(
                    f"DEBUG: Exception in process_upgrade_session for {session_id}: {str(e)}"
                )
                logger.error(
                    f"Upgrade simulation for session {session_id} failed: {str(e)}"
                )
        finally:
            loop.close()
            print(f"DEBUG: Thread for session {session_id} finished")
            # Clean up the task reference
            if session_id in active_simulations:
                del active_simulations[session_id]

    # Create a thread for the task
    thread = threading.Thread(target=run_async_task, daemon=True)
    thread.start()

    # Store a reference to the thread
    active_simulations[session_id] = thread

    # Set initial session state if not already set
    if session_id in upgrade_sessions:
        session = upgrade_sessions[session_id]
        if "startTime" not in session:
            session["startTime"] = datetime.now().isoformat()
        if "messages" not in session:
            session["messages"] = []

    logger.info(f"Started upgrade simulation task for session {session_id}")


def stop_upgrade_simulation(session_id: str):
    """Stop an ongoing upgrade simulation."""
    if session_id not in active_simulations:
        logger.warning(f"No active simulation found for session {session_id}")
        return

    # Mark the session as failed if it exists
    if session_id in upgrade_sessions:
        upgrade_sessions[session_id]["status"] = UpgradeStatusEnum.FAILED
        upgrade_sessions[session_id]["messages"].append(
            {
                "timestamp": datetime.now().isoformat(),
                "message": "Upgrade simulation was cancelled",
                "severity": 1,
            }
        )

    # For Thread objects, we can't cancel them directly, but we can mark the session as failed
    # which will cause the thread to exit gracefully when it checks the session status
    logger.info(
        f"Task {session_id} stopped: simulation for session {session_id} was stopped"
    )

    # Remove from active simulations
    if session_id in active_simulations:
        del active_simulations[session_id]

    logger.info(f"Stopped upgrade simulation for session {session_id}")
