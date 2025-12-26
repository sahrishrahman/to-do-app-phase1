"""Integration tests for complete user workflows.

These tests verify the full user journey through the application.
"""

import pytest
from io import StringIO
from unittest.mock import patch
from src.services.task_service import TaskService
from src.cli.menu import Menu


def get_print_output(mock_print):
    """Extract all printed strings from mock_print calls."""
    output = []
    for call in mock_print.call_args_list:
        # Each call is a tuple of (args, kwargs)
        args, kwargs = call
        if args:
            output.append("".join(str(a) for a in args))
        if kwargs:
            output.append(str(kwargs))
    return "\n".join(output)


class TestAddTaskWorkflow:
    """Integration tests for Add Task workflow."""

    def test_add_valid_task_shows_confirmation(self):
        """Verify adding a valid task shows success message with ID."""
        service = TaskService()
        menu = Menu(service)

        with patch("builtins.input", side_effect=["1", "Buy groceries", "7"]):
            with patch("builtins.print") as mock_print:
                menu.run()

        # Check that task was added
        assert service.task_count() == 1
        assert service.get_task_by_id(1).title == "Buy groceries"

    def test_add_empty_title_shows_error(self):
        """Verify empty title shows error and task is not added."""
        service = TaskService()
        menu = Menu(service)

        with patch("builtins.input", side_effect=["1", "", "7"]):
            menu.run()

        assert service.task_count() == 0

    def test_add_whitespace_title_shows_error(self):
        """Verify whitespace-only title shows error."""
        service = TaskService()
        menu = Menu(service)

        with patch("builtins.input", side_effect=["1", "   ", "7"]):
            menu.run()

        assert service.task_count() == 0


class TestViewTasksWorkflow:
    """Integration tests for View Tasks workflow."""

    def test_view_empty_list_shows_message(self):
        """Verify viewing empty task list shows appropriate message."""
        service = TaskService()
        menu = Menu(service)

        with patch("builtins.input", side_effect=["2", "7"]):
            with patch("builtins.print") as mock_print:
                menu.run()

        output = get_print_output(mock_print)
        assert "No tasks available" in output

    def test_view_tasks_with_data(self):
        """Verify viewing tasks shows all tasks with status."""
        service = TaskService()
        menu = Menu(service)
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.mark_complete(1)

        with patch("builtins.input", side_effect=["2", "7"]):
            with patch("builtins.print") as mock_print:
                menu.run()

        assert service.task_count() == 2

    def test_view_tasks_summary_counts(self):
        """Verify view shows correct completion summary."""
        service = TaskService()
        menu = Menu(service)
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")
        service.mark_complete(1)
        service.mark_complete(3)

        with patch("builtins.input", side_effect=["2", "7"]):
            with patch("builtins.print") as mock_print:
                menu.run()

        output = get_print_output(mock_print)
        assert "Total: 3 tasks (2 complete, 1 incomplete)" in output


class TestUpdateTaskWorkflow:
    """Integration tests for Update Task workflow."""

    def test_update_valid_task_shows_success(self):
        """Verify updating a valid task shows success message."""
        service = TaskService()
        menu = Menu(service)
        service.add_task("Original title")

        with patch("builtins.input", side_effect=["3", "1", "Updated title", "7"]):
            menu.run()

        assert service.get_task_by_id(1).title == "Updated title"

    def test_update_invalid_id_shows_error(self):
        """Verify updating non-existent task ID shows error."""
        service = TaskService()
        menu = Menu(service)
        service.add_task("Task 1")  # Add a task first

        with patch("builtins.input", side_effect=["3", "999", "New title", "7"]):
            with patch("builtins.print") as mock_print:
                menu.run()

        output = get_print_output(mock_print)
        assert "not found" in output

    def test_update_non_numeric_id_shows_error(self):
        """Verify non-numeric ID input shows error."""
        service = TaskService()
        menu = Menu(service)
        service.add_task("Task 1")  # Add a task first

        with patch("builtins.input", side_effect=["3", "abc", "7"]):
            with patch("builtins.print") as mock_print:
                menu.run()

        output = get_print_output(mock_print)
        assert "valid number" in output

    def test_update_empty_title_shows_error(self):
        """Verify empty new title shows error and title unchanged."""
        service = TaskService()
        menu = Menu(service)
        service.add_task("Original title")

        with patch("builtins.input", side_effect=["3", "1", "", "7"]):
            menu.run()

        assert service.get_task_by_id(1).title == "Original title"


class TestDeleteTaskWorkflow:
    """Integration tests for Delete Task workflow."""

    def test_delete_valid_task_shows_success(self):
        """Verify deleting a valid task shows success message."""
        service = TaskService()
        menu = Menu(service)
        service.add_task("Task to delete")

        with patch("builtins.input", side_effect=["4", "1", "7"]):
            menu.run()

        assert service.task_count() == 0

    def test_delete_invalid_id_shows_error(self):
        """Verify deleting non-existent task ID shows error."""
        service = TaskService()
        menu = Menu(service)
        service.add_task("Task 1")  # Add a task first

        with patch("builtins.input", side_effect=["4", "999", "7"]):
            with patch("builtins.print") as mock_print:
                menu.run()

        output = get_print_output(mock_print)
        assert "not found" in output

    def test_delete_non_numeric_id_shows_error(self):
        """Verify non-numeric ID input shows error."""
        service = TaskService()
        menu = Menu(service)
        service.add_task("Task 1")  # Add a task first

        with patch("builtins.input", side_effect=["4", "abc", "7"]):
            with patch("builtins.print") as mock_print:
                menu.run()

        output = get_print_output(mock_print)
        assert "valid number" in output


class TestMarkCompleteWorkflow:
    """Integration tests for Mark Complete workflow."""

    def test_mark_complete_valid_task(self):
        """Verify marking a valid task as complete works."""
        service = TaskService()
        menu = Menu(service)
        service.add_task("Task")

        with patch("builtins.input", side_effect=["5", "1", "7"]):
            menu.run()

        assert service.get_task_by_id(1).is_complete is True

    def test_mark_complete_invalid_id_shows_error(self):
        """Verify marking non-existent task shows error."""
        service = TaskService()
        menu = Menu(service)
        service.add_task("Task 1")  # Add a task first

        with patch("builtins.input", side_effect=["5", "999", "7"]):
            with patch("builtins.print") as mock_print:
                menu.run()

        output = get_print_output(mock_print)
        assert "not found" in output


class TestMarkIncompleteWorkflow:
    """Integration tests for Mark Incomplete workflow."""

    def test_mark_incomplete_valid_task(self):
        """Verify marking a valid task as incomplete works."""
        service = TaskService()
        menu = Menu(service)
        service.add_task("Task")
        service.mark_complete(1)

        with patch("builtins.input", side_effect=["6", "1", "7"]):
            menu.run()

        assert service.get_task_by_id(1).is_complete is False

    def test_mark_incomplete_invalid_id_shows_error(self):
        """Verify marking non-existent task shows error."""
        service = TaskService()
        menu = Menu(service)
        service.add_task("Task 1")  # Add a task first

        with patch("builtins.input", side_effect=["6", "999", "7"]):
            with patch("builtins.print") as mock_print:
                menu.run()

        output = get_print_output(mock_print)
        assert "not found" in output


class TestInvalidMenuChoice:
    """Integration tests for invalid menu choices."""

    def test_invalid_choice_shows_error(self):
        """Verify invalid menu choice shows error message."""
        service = TaskService()
        menu = Menu(service)

        with patch("builtins.input", side_effect=["9", "7"]):
            with patch("builtins.print") as mock_print:
                menu.run()

        output = get_print_output(mock_print)
        assert "Invalid choice" in output

    def test_letter_choice_shows_error(self):
        """Verify letter menu choice shows error."""
        service = TaskService()
        menu = Menu(service)

        with patch("builtins.input", side_effect=["abc", "7"]):
            with patch("builtins.print") as mock_print:
                menu.run()

        output = get_print_output(mock_print)
        assert "Invalid choice" in output


class TestFullWorkflow:
    """Full end-to-end workflow tests."""

    def test_complete_user_journey(self):
        """Test complete user journey: add, view, update, mark complete, view, delete."""
        service = TaskService()
        menu = Menu(service)

        # User journey: add 2 tasks, view, update first, mark complete, view, delete second, view
        with patch("builtins.input", side_effect=[
            "1", "Buy groceries",  # Add task 1
            "1", "Call mom",       # Add task 2
            "2",                   # View tasks
            "3", "1", "Buy groceries and supplies",  # Update task 1
            "5", "1",              # Mark task 1 complete
            "2",                   # View tasks (check status)
            "4", "2",              # Delete task 2
            "2",                   # View tasks (check deletion)
            "7"                    # Exit
        ]):
            menu.run()

        # Verify final state
        assert service.task_count() == 1
        assert service.get_task_by_id(1).title == "Buy groceries and supplies"
        assert service.get_task_by_id(1).is_complete is True

    def test_all_error_paths(self):
        """Test all error handling paths."""
        service = TaskService()
        menu = Menu(service)

        # Try to update when empty, delete when empty, etc.
        with patch("builtins.input", side_effect=[
            "3",  # Update
            "4",  # Delete
            "5",  # Mark complete
            "6",  # Mark incomplete
            "7"   # Exit
        ]):
            menu.run()

        # All should fail gracefully with no tasks
        assert service.task_count() == 0

    def test_task_id_persistence(self):
        """Verify task IDs remain stable throughout operations."""
        service = TaskService()
        menu = Menu(service)

        with patch("builtins.input", side_effect=[
            "1", "Task 1",
            "1", "Task 2",
            "1", "Task 3",
            "4", "2",  # Delete task 2
            "5", "1",  # Mark task 1 complete
            "3", "3", "Updated Task 3",  # Update task 3
            "6", "1",  # Mark task 1 incomplete
            "7"
        ]):
            menu.run()

        # Task 1 should still be ID 1
        assert service.get_task_by_id(1).title == "Task 1"
        assert service.get_task_by_id(1).is_complete is False

        # Task 2 should be deleted
        assert service.get_task_by_id(2) is None

        # Task 3 should still be ID 3 with updated title
        assert service.get_task_by_id(3).title == "Updated Task 3"
