"""Small TaskPulse domain logic for CI demonstration."""


def calculate_completion_rate(done_tasks: int, total_tasks: int) -> float:
    """Return completed task percentage rounded to two digits."""
    if done_tasks < 0:
        raise ValueError("done_tasks cannot be negative")
    if total_tasks <= 0:
        raise ValueError("total_tasks must be positive")
    if done_tasks > total_tasks:
        raise ValueError("done_tasks cannot exceed total_tasks")

    return round(done_tasks / total_tasks * 100, 2)


def task_status(done_tasks: int, total_tasks: int) -> str:
    """Return board status from completed and total tasks."""
    rate = calculate_completion_rate(done_tasks, total_tasks)
    if rate == 100:
        return "done"
    if rate >= 50:
        return "in_progress"

    return "backlog"


def has_wip_limit_violation(in_progress_tasks: int, wip_limit: int = 3) -> bool:
    """Check whether the board has too many tasks in progress."""
    if in_progress_tasks < 0:
        raise ValueError("in_progress_tasks cannot be negative")
    if wip_limit <= 0:
        raise ValueError("wip_limit must be positive")

    return in_progress_tasks > wip_limit

x=1