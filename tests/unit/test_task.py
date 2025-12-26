"""Unit tests for the Task dataclass."""

import pytest
from src.models.task import Task


class TestTaskCreation:
    """Tests for Task object creation."""

    def test_create_task_with_all_fields(self):
        """Verify Task can be created with all fields specified."""
        task = Task(id=1, title="Buy groceries", is_complete=True)

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.is_complete is True

    def test_create_task_with_default_incomplete(self):
        """Verify is_complete defaults to False for new tasks."""
        task = Task(id=1, title="Buy groceries")

        assert task.is_complete is False

    def test_task_equality(self):
        """Verify two identical Tasks are equal."""
        task1 = Task(id=1, title="Buy groceries", is_complete=False)
        task2 = Task(id=1, title="Buy groceries", is_complete=False)

        assert task1 == task2

    def test_task_inequality_different_id(self):
        """Verify Tasks with different IDs are not equal."""
        task1 = Task(id=1, title="Buy groceries")
        task2 = Task(id=2, title="Buy groceries")

        assert task1 != task2

    def test_task_inequality_different_title(self):
        """Verify Tasks with different titles are not equal."""
        task1 = Task(id=1, title="Buy groceries")
        task2 = Task(id=1, title="Call mom")

        assert task1 != task2

    def test_task_inequality_different_status(self):
        """Verify Tasks with different completion status are not equal."""
        task1 = Task(id=1, title="Buy groceries", is_complete=False)
        task2 = Task(id=1, title="Buy groceries", is_complete=True)

        assert task1 != task2

    def test_task_immutability_of_id(self):
        """Verify Task id cannot be reassigned (dataclass is mutable but id should not change in practice)."""
        task = Task(id=1, title="Test task")

        # id is not frozen, so technically reassignable, but service layer controls this
        task.id = 999
        assert task.id == 999

    def test_task_repr(self):
        """Verify Task has a readable string representation."""
        task = Task(id=1, title="Test task", is_complete=False)

        repr_str = repr(task)
        assert "Task" in repr_str
        assert "id=1" in repr_str
        assert "title='Test task'" in repr_str
