"""TaskService - Handles all task operations with in-memory storage."""

from typing import List, Optional
from src.models.task import Task


class TaskService:
    """Handles all task operations with in-memory storage.

    All tasks are stored in a simple list and lost when the application exits.
    Task IDs are assigned sequentially starting from 1.
    """

    def __init__(self):
        """Initialize the TaskService with empty storage."""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str) -> Task:
        """Create a new task with a unique ID.

        Args:
            title: The task description.

        Returns:
            The newly created Task object.
        """
        task = Task(id=self._next_id, title=title, is_complete=False)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks in insertion order.

        Returns:
            A copy of the task list to prevent external modification.
        """
        return self._tasks.copy()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Find a task by its ID.

        Args:
            task_id: The ID of the task to find.

        Returns:
            The Task if found, None otherwise.
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task_title(self, task_id: int, new_title: str) -> bool:
        """Update a task's title.

        Args:
            task_id: The ID of the task to update.
            new_title: The new title for the task.

        Returns:
            True if the task was found and updated, False otherwise.
        """
        for task in self._tasks:
            if task.id == task_id:
                task.title = new_title
                return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if the task was found and deleted, False otherwise.
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                return True
        return False

    def mark_complete(self, task_id: int) -> bool:
        """Mark a task as complete.

        Args:
            task_id: The ID of the task to mark complete.

        Returns:
            True if the task was found and updated, False otherwise.
        """
        for task in self._tasks:
            if task.id == task_id:
                task.is_complete = True
                return True
        return False

    def mark_incomplete(self, task_id: int) -> bool:
        """Mark a task as incomplete.

        Args:
            task_id: The ID of the task to mark incomplete.

        Returns:
            True if the task was found and updated, False otherwise.
        """
        for task in self._tasks:
            if task.id == task_id:
                task.is_complete = False
                return True
        return False

    def task_count(self) -> int:
        """Return the number of tasks in storage.

        Returns:
            The count of tasks.
        """
        return len(self._tasks)
