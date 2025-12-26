"""Task entity representing a single todo item."""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique identifier for the task, assigned sequentially.
        title: Description of the task.
        is_complete: Whether the task has been completed.
    """

    id: int
    title: str
    is_complete: bool = False
