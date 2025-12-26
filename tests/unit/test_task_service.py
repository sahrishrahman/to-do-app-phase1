"""Unit tests for the TaskService class."""

import pytest
from src.services.task_service import TaskService
from src.models.task import Task


class TestTaskServiceInitialization:
    """Tests for TaskService initialization."""

    def test_initial_empty_storage(self):
        """Verify TaskService starts with empty task list."""
        service = TaskService()

        assert service.task_count() == 0
        assert service.get_all_tasks() == []

    def test_initial_next_id_is_one(self):
        """Verify first task will get ID 1."""
        service = TaskService()

        # Add a task and verify it gets ID 1
        task = service.add_task("First task")
        assert task.id == 1


class TestAddTask:
    """Tests for TaskService.add_task()."""

    def test_add_single_task(self):
        """Verify adding a single task creates it with ID 1."""
        service = TaskService()

        task = service.add_task("Buy groceries")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.is_complete is False

    def test_add_multiple_tasks_sequential_ids(self):
        """Verify adding multiple tasks gets sequential IDs."""
        service = TaskService()

        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_default_incomplete(self):
        """Verify new tasks are marked incomplete by default."""
        service = TaskService()

        task = service.add_task("New task")

        assert task.is_complete is False

    def test_add_task_stored_in_service(self):
        """Verify added task is stored and retrievable."""
        service = TaskService()

        service.add_task("Stored task")
        tasks = service.get_all_tasks()

        assert len(tasks) == 1
        assert tasks[0].title == "Stored task"


class TestGetAllTasks:
    """Tests for TaskService.get_all_tasks()."""

    def test_get_empty_tasks(self):
        """Verify returns empty list when no tasks exist."""
        service = TaskService()

        tasks = service.get_all_tasks()

        assert tasks == []

    def test_get_all_tasks_returns_copy(self):
        """Verify get_all_tasks returns a copy, not the original list."""
        service = TaskService()
        service.add_task("Task 1")

        tasks = service.get_all_tasks()
        tasks.clear()  # Modify the returned list

        # Original should be unchanged
        assert len(service.get_all_tasks()) == 1

    def test_get_all_tasks_preserves_order(self):
        """Verify tasks are returned in insertion order."""
        service = TaskService()
        service.add_task("First")
        service.add_task("Second")
        service.add_task("Third")

        tasks = service.get_all_tasks()

        assert len(tasks) == 3
        assert tasks[0].title == "First"
        assert tasks[1].title == "Second"
        assert tasks[2].title == "Third"


class TestGetTaskById:
    """Tests for TaskService.get_task_by_id()."""

    def test_get_existing_task(self):
        """Verify retrieving an existing task returns it."""
        service = TaskService()
        service.add_task("Task 1")
        service.add_task("Task 2")

        task = service.get_task_by_id(2)

        assert task is not None
        assert task.id == 2
        assert task.title == "Task 2"

    def test_get_nonexistent_task(self):
        """Verify retrieving non-existent task returns None."""
        service = TaskService()

        task = service.get_task_by_id(999)

        assert task is None

    def test_get_task_after_deletion(self):
        """Verify cannot get a deleted task."""
        service = TaskService()
        service.add_task("Task 1")
        service.delete_task(1)

        task = service.get_task_by_id(1)

        assert task is None


class TestUpdateTaskTitle:
    """Tests for TaskService.update_task_title()."""

    def test_update_existing_task(self):
        """Verify updating an existing task returns True."""
        service = TaskService()
        service.add_task("Old title")

        result = service.update_task_title(1, "New title")

        assert result is True
        assert service.get_task_by_id(1).title == "New title"

    def test_update_nonexistent_task(self):
        """Verify updating non-existent task returns False."""
        service = TaskService()

        result = service.update_task_title(999, "New title")

        assert result is False

    def test_update_does_not_change_id(self):
        """Verify updating title does not change task ID."""
        service = TaskService()
        service.add_task("Original")

        service.update_task_title(1, "Updated")

        task = service.get_task_by_id(1)
        assert task.id == 1
        assert task.title == "Updated"


class TestDeleteTask:
    """Tests for TaskService.delete_task()."""

    def test_delete_existing_task(self):
        """Verify deleting an existing task returns True."""
        service = TaskService()
        service.add_task("Task to delete")

        result = service.delete_task(1)

        assert result is True
        assert service.task_count() == 0

    def test_delete_nonexistent_task(self):
        """Verify deleting non-existent task returns False."""
        service = TaskService()

        result = service.delete_task(999)

        assert result is False

    def test_delete_preserves_other_tasks(self):
        """Verify deleting one task preserves others."""
        service = TaskService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")

        service.delete_task(2)

        assert service.task_count() == 2
        assert service.get_task_by_id(1) is not None
        assert service.get_task_by_id(2) is None
        assert service.get_task_by_id(3) is not None

    def test_delete_id_not_reused(self):
        """Verify deleted task ID is not reused for new tasks."""
        service = TaskService()
        service.add_task("Task 1")
        service.delete_task(1)
        service.add_task("New task")

        new_task = service.get_task_by_id(2)
        assert new_task is not None
        assert new_task.id == 2


class TestMarkComplete:
    """Tests for TaskService.mark_complete()."""

    def test_mark_complete_existing(self):
        """Verify marking existing task complete returns True."""
        service = TaskService()
        service.add_task("Task")

        result = service.mark_complete(1)

        assert result is True
        assert service.get_task_by_id(1).is_complete is True

    def test_mark_complete_nonexistent(self):
        """Verify marking non-existent task complete returns False."""
        service = TaskService()

        result = service.mark_complete(999)

        assert result is False

    def test_mark_complete_already_complete(self):
        """Verify marking already complete task still returns True."""
        service = TaskService()
        service.add_task("Task")
        service.mark_complete(1)

        result = service.mark_complete(1)

        assert result is True


class TestMarkIncomplete:
    """Tests for TaskService.mark_incomplete()."""

    def test_mark_incomplete_existing(self):
        """Verify marking existing task incomplete returns True."""
        service = TaskService()
        service.add_task("Task")
        service.mark_complete(1)

        result = service.mark_incomplete(1)

        assert result is True
        assert service.get_task_by_id(1).is_complete is False

    def test_mark_incomplete_nonexistent(self):
        """Verify marking non-existent task incomplete returns False."""
        service = TaskService()

        result = service.mark_incomplete(999)

        assert result is False

    def test_mark_incomplete_already_incomplete(self):
        """Verify marking already incomplete task still returns True."""
        service = TaskService()
        service.add_task("Task")

        result = service.mark_incomplete(1)

        assert result is True


class TestTaskServiceIntegration:
    """Integration tests combining multiple operations."""

    def test_full_crud_workflow(self):
        """Test complete Create, Read, Update, Delete workflow."""
        service = TaskService()

        # Create
        task1 = service.add_task("Buy groceries")
        task2 = service.add_task("Call mom")

        assert service.task_count() == 2

        # Read
        assert service.get_task_by_id(1).title == "Buy groceries"

        # Update
        service.update_task_title(1, "Buy groceries and supplies")

        assert service.get_task_by_id(1).title == "Buy groceries and supplies"

        # Delete
        service.delete_task(1)

        assert service.task_count() == 1
        assert service.get_task_by_id(1) is None
        assert service.get_task_by_id(2) is not None

    def test_complete_incomplete_workflow(self):
        """Test marking tasks complete and incomplete."""
        service = TaskService()
        service.add_task("Task 1")
        service.add_task("Task 2")

        # Mark first complete
        service.mark_complete(1)

        assert service.get_task_by_id(1).is_complete is True
        assert service.get_task_by_id(2).is_complete is False

        # Mark second complete
        service.mark_complete(2)

        assert service.get_task_by_id(1).is_complete is True
        assert service.get_task_by_id(2).is_complete is True

        # Mark first incomplete
        service.mark_incomplete(1)

        assert service.get_task_by_id(1).is_complete is False
        assert service.get_task_by_id(2).is_complete is True
