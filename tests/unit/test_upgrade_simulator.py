"""Unit tests for the upgrade simulator module."""

import asyncio
from datetime import datetime, timedelta

import pytest

from dell_unisphere_package.models.storage import (
    candidate_software_versions,
    upgrade_sessions,
    uploaded_files,
)
from dell_unisphere_package.schemas.base import TaskStatusEnum, UpgradeStatusEnum
from dell_unisphere_package.utils.upgrade_simulator import (
    active_simulations,
    create_realistic_upgrade_tasks,
    format_timedelta,
    parse_time_to_seconds,
    process_upgrade_session,
    start_upgrade_simulation,
    stop_upgrade_simulation,
)


def test_parse_time_to_seconds():
    """Test parsing time strings to seconds."""
    assert parse_time_to_seconds("00:00:30.000") == 30
    assert parse_time_to_seconds("00:01:00.000") == 60
    assert parse_time_to_seconds("01:00:00.000") == 3600
    assert parse_time_to_seconds("01:30:45.000") == 5445


def test_format_timedelta():
    """Test formatting timedelta to ISO 8601 duration format."""
    assert format_timedelta(timedelta(seconds=30)) == "PT0H0M30S"
    assert format_timedelta(timedelta(minutes=5)) == "PT0H5M0S"
    assert format_timedelta(timedelta(hours=2)) == "PT2H0M0S"
    assert format_timedelta(timedelta(hours=1, minutes=30, seconds=45)) == "PT1H30M45S"


def test_create_realistic_upgrade_tasks():
    """Test creating realistic upgrade tasks."""
    tasks = create_realistic_upgrade_tasks()

    # Verify we have the expected number of tasks
    assert len(tasks) == 12

    # Verify task structure
    for task in tasks:
        assert "status" in task
        assert "type" in task
        assert "caption" in task
        assert "creationTime" in task
        assert "estRemainTime" in task

        # All tasks should be in PENDING state initially
        assert task["status"] == TaskStatusEnum.PENDING

    # Verify specific task captions
    assert tasks[0]["caption"] == "Preparing system"
    assert tasks[5]["caption"] == "Installing new software on peer SP"
    assert tasks[-1]["caption"] == "Final tasks"

    # Verify estimated time format
    for task in tasks:
        est_time = task["estRemainTime"]
        # Should be in format HH:MM:SS.mmm
        assert len(est_time.split(":")) == 3
        hours, minutes, seconds_ms = est_time.split(":")
        assert len(hours) == 2
        assert len(minutes) == 2
        assert "." in seconds_ms


# Use pytest-asyncio's built-in event_loop fixture with module scope
# This avoids the deprecation warning about redefining the event_loop fixture


@pytest.fixture
def reset_storage():
    """Reset storage before and after each test."""
    upgrade_sessions.clear()
    candidate_software_versions.clear()
    uploaded_files.clear()
    active_simulations.clear()
    yield
    upgrade_sessions.clear()
    candidate_software_versions.clear()
    uploaded_files.clear()
    active_simulations.clear()


@pytest.fixture
def session_id():
    """Create a test session ID."""
    return "test_session_123"


@pytest.fixture
def upgrade_session(session_id):
    """Create a test upgrade session with simplified tasks for testing."""
    # Create simple tasks that complete quickly for testing
    simple_tasks = [
        {
            "name": "Test Task 1",
            "caption": "Test Task 1",
            "status": TaskStatusEnum.PENDING,
            "estimatedTime": "00:03:01.000",
            "startTime": None,
            "endTime": None,
        },
        {
            "name": "Test Task 2",
            "caption": "Test Task 2",
            "status": TaskStatusEnum.PENDING,
            "estimatedTime": "00:03:01.000",
            "startTime": None,
            "endTime": None,
        },
    ]

    session = {
        "id": session_id,
        "status": UpgradeStatusEnum.NOT_STARTED,
        "percentComplete": 0,
        "startTime": datetime.now().isoformat(),
        "tasks": simple_tasks,
        "messages": [],
        "candidate": "test_candidate_123",
    }
    upgrade_sessions[session_id] = session
    return session


@pytest.fixture
def candidate_software():
    """Create a test candidate software version."""
    candidate_id = "test_candidate_123"
    candidate = {
        "id": candidate_id,
        "fullVersion": "Unity test.bin",
        "rebootRequired": True,
        "canPauseBeforeReboot": True,
    }
    candidate_software_versions[candidate_id] = candidate
    return candidate


@pytest.mark.asyncio
async def test_process_upgrade_session_completion(
    reset_storage, upgrade_session, candidate_software, session_id
):
    """Test that upgrade session completes successfully and removes candidate."""
    # Capture initial state
    initial_session = upgrade_sessions[session_id].copy()
    assert initial_session["status"] == UpgradeStatusEnum.NOT_STARTED
    assert initial_session["percentComplete"] == 0
    for task in initial_session["tasks"]:
        assert task["status"] == TaskStatusEnum.PENDING
        assert task["startTime"] is None
        assert task["endTime"] is None

    # Store initial message count to verify new messages are added
    initial_message_count = len(upgrade_sessions[session_id]["messages"])

    # Run the upgrade process
    try:
        await asyncio.wait_for(process_upgrade_session(session_id), timeout=10.0)
    except asyncio.TimeoutError:
        pytest.fail("Upgrade did not complete in time")

    # Verify final session state
    final_session = upgrade_sessions[session_id]
    assert final_session["status"] == UpgradeStatusEnum.COMPLETED
    assert final_session["percentComplete"] == 100
    assert "startTime" in final_session
    assert "elapsedTime" in final_session

    # Verify all tasks completed in the right order
    for i, task in enumerate(final_session["tasks"]):
        assert (
            task["status"] == TaskStatusEnum.COMPLETED
        ), f"Task {i+1} did not complete"
        assert task["startTime"] is not None, f"Task {i+1} has no start time"
        assert task["endTime"] is not None, f"Task {i+1} has no end time"

        # If not the first task, verify sequential execution
        if i > 0:
            prev_task = final_session["tasks"][i - 1]
            # The current task should start after or at the same time as the previous task ends
            assert (
                task["startTime"] >= prev_task["endTime"]
            ), f"Task {i+1} started before Task {i} completed"

    # Verify messages were added during the process
    assert len(final_session["messages"]) > initial_message_count

    # Verify there are task start and completion messages
    task_start_messages = [
        msg
        for msg in final_session["messages"]
        if "started" in msg["message"].lower() or "starting" in msg["message"].lower()
    ]
    task_complete_messages = [
        msg
        for msg in final_session["messages"]
        if "completed" in msg["message"].lower() or "complete" in msg["message"].lower()
    ]

    assert len(task_start_messages) >= len(
        final_session["tasks"]
    ), "Not all tasks have start messages"
    assert len(task_complete_messages) >= len(
        final_session["tasks"]
    ), "Not all tasks have completion messages"

    # Verify candidate was removed after successful upgrade
    assert len(candidate_software_versions) == 0, "Candidate software was not removed"
    assert len(uploaded_files) == 0, "Uploaded files were not cleaned up"


@pytest.mark.asyncio
async def test_process_upgrade_session_failure(
    reset_storage, upgrade_session, session_id
):
    """Test upgrade session failure handling."""
    # Simulate a failure by removing the candidate before completion
    candidate_software_versions.clear()

    # Start the upgrade simulation and expect it to fail
    try:
        await asyncio.wait_for(process_upgrade_session(session_id), timeout=5.0)
        pytest.fail("Expected the upgrade to fail but it completed successfully")
    except Exception:
        # Expected exception - the upgrade should fail
        pass

    # Verify session failed
    assert upgrade_sessions[session_id]["status"] == UpgradeStatusEnum.FAILED
    assert any(msg["severity"] == 2 for msg in upgrade_sessions[session_id]["messages"])


@pytest.mark.asyncio
async def test_start_stop_upgrade_simulation(
    reset_storage, upgrade_session, session_id
):
    """Test starting and stopping upgrade simulations."""
    # Start simulation
    start_upgrade_simulation(session_id)
    assert session_id in active_simulations
    assert active_simulations[
        session_id
    ].is_alive()  # Thread objects use is_alive() instead of done()

    # Give the task a moment to start
    await asyncio.sleep(0.1)

    # Try starting again (should not create new task)
    start_upgrade_simulation(session_id)
    assert len(active_simulations) == 1

    # Stop simulation
    stop_upgrade_simulation(session_id)

    # Wait a moment for cleanup
    await asyncio.sleep(0.1)

    assert session_id not in active_simulations

    # Try stopping again (should not raise error)
    stop_upgrade_simulation(session_id)


@pytest.mark.asyncio
async def test_upgrade_session_pause_resume(
    reset_storage, upgrade_session, candidate_software, session_id
):
    """Test pausing and resuming upgrade session."""
    # Start with a paused session
    upgrade_sessions[session_id]["status"] = UpgradeStatusEnum.PAUSED

    # Create a future to control the test flow
    resume_future = asyncio.Future()

    async def run_session_with_pause():
        # Start the process and handle the pause
        session_task = asyncio.create_task(process_upgrade_session(session_id))

        # Wait a bit to ensure task starts
        await asyncio.sleep(0.1)

        # Verify session is still paused
        assert upgrade_sessions[session_id]["status"] == UpgradeStatusEnum.PAUSED

        # Resume the session
        upgrade_sessions[session_id]["status"] = UpgradeStatusEnum.IN_PROGRESS

        # Wait for completion
        try:
            await asyncio.wait_for(session_task, timeout=10.0)
            resume_future.set_result(True)
        except asyncio.TimeoutError:
            session_task.cancel()
            resume_future.set_exception(
                asyncio.TimeoutError("Upgrade did not complete in time")
            )
        except Exception as e:
            resume_future.set_exception(e)

    # Start the background task
    asyncio.create_task(run_session_with_pause())

    # Wait for the test to complete
    try:
        await asyncio.wait_for(resume_future, timeout=15.0)
    except asyncio.TimeoutError:
        pytest.fail("Upgrade did not complete in time")
    except Exception as e:
        pytest.fail(f"Upgrade failed: {str(e)}")

    # Verify session completed
    assert upgrade_sessions[session_id]["status"] == UpgradeStatusEnum.COMPLETED
    assert upgrade_sessions[session_id]["percentComplete"] == 100

    # Verify all tasks are completed
    for task in upgrade_sessions[session_id]["tasks"]:
        assert task["status"] == TaskStatusEnum.COMPLETED
        assert "endTime" in task

    # Verify candidate was removed
    assert len(candidate_software_versions) == 0
    assert len(uploaded_files) == 0
