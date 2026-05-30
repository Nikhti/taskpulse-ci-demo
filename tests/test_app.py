"""Unit tests for TaskPulse demo logic."""

import pytest

from src.app import calculate_completion_rate, has_wip_limit_violation, task_status


def test_calculate_completion_rate():
    assert calculate_completion_rate(3, 4) == 75.0


def test_calculate_completion_rate_rejects_zero_total():
    with pytest.raises(ValueError, match="total_tasks must be positive"):
        calculate_completion_rate(1, 0)


def test_task_status_done():
    assert task_status(5, 5) == "done"


def test_task_status_in_progress():
    assert task_status(2, 4) == "in_progress"


def test_task_status_backlog():
    assert task_status(1, 5) == "backlog"


def test_wip_limit_violation():
    assert has_wip_limit_violation(4, wip_limit=3) is True


def test_no_wip_limit_violation():
    assert has_wip_limit_violation(2, wip_limit=3) is False
