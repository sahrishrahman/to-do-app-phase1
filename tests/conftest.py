"""Pytest configuration and shared fixtures for tests."""

import pytest
from src.services.task_service import TaskService
from src.models.task import Task


@pytest.fixture
def empty_service():
    """Return a fresh TaskService with no tasks."""
    return TaskService()


@pytest.fixture
def service_with_tasks(empty_service):
    """Return a TaskService with three sample tasks."""
    empty_service.add_task("Buy groceries")
    empty_service.add_task("Call mom")
    empty_service.add_task("Finish report")
    return empty_service


@pytest.fixture
def sample_task():
    """Return a sample Task object."""
    return Task(id=1, title="Sample task", is_complete=False)


@pytest.fixture
def completed_task():
    """Return a completed Task object."""
    return Task(id=1, title="Completed task", is_complete=True)
