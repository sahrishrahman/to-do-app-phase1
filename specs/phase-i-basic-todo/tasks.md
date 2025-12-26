# Implementation Tasks: Phase I - Basic In-Memory Todo Application

**Branch**: `phase-i-basic-todo`
**Date**: 2025-12-25
**Spec**: `specs/phase-i-basic-todo/spec.md`
**Plan**: `specs/phase-i-basic-todo/plan.md`

---

## Task 001: Create Project Directory Structure

**Description**: Create the required directory structure for the Phase I application.

**Preconditions**:
- Project root exists (`todo-app/`)

**Expected Output**:
- Directories created:
  - `src/`
  - `src/models/`
  - `src/services/`
  - `src/cli/`
  - `tests/`
  - `tests/unit/`
  - `tests/integration/`

**Artifacts**:
- Created: `src/__init__.py`
- Created: `src/models/__init__.py`
- Created: `src/services/__init__.py`
- Created: `src/cli/__init__.py`
- Created: `tests/__init__.py`
- Created: `tests/unit/__init__.py`
- Created: `tests/integration/__init__.py`

**References**:
- Plan: "Source Code Structure" section
- Plan: "Files to Create (in order)" item 1-6

---

## Task 002: Implement Task Data Model

**Description**: Create the Task dataclass representing a single todo item with id, title, and is_complete fields.

**Preconditions**:
- `src/models/__init__.py` exists
- `src/models/task.py` does not exist

**Expected Output**:
- `Task` dataclass with three fields:
  - `id: int` - Unique task identifier
  - `title: str` - Task description
  - `is_complete: bool` - Completion status, defaults to False

**Artifacts**:
- Created: `src/models/task.py`

**Code Requirements**:
```python
from dataclasses import dataclass

@dataclass
class Task:
    """Represents a single todo task."""
    id: int
    title: str
    is_complete: bool = False
```

**References**:
- Spec: "Task Entity" section under "Data Model"
- Spec: "Task dataclass with id, title, is_complete fields"
- Plan: "Data Model Layer" section with code example

**Testable By**:
- Running `python -c "from src.models.task import Task; t = Task(1, 'Test', False); print(t.id, t.title, t.is_complete)"`

---

## Task 003: Create requirements.txt

**Description**: Create requirements.txt with only pytest for testing.

**Preconditions**:
- `requirements.txt` does not exist

**Expected Output**:
- `requirements.txt` containing only `pytest`

**Artifacts**:
- Created: `requirements.txt`

**Content**:
```
pytest
```

**References**:
- Plan: "Files to Create (in order)" item 9

---

## Task 004: Write Unit Tests for Task Data Model

**Description**: Write unit tests for the Task dataclass covering creation, default values, and equality.

**Preconditions**:
- `src/models/task.py` exists (from Task 002)
- `tests/unit/test_task.py` does not exist

**Expected Output**:
- Test file with tests for:
  - Task creation with all fields
  - Task creation with default is_complete=False
  - Task equality comparison
  - Task inequality comparison

**Artifacts**:
- Created: `tests/unit/test_task.py`

**Test Cases**:
1. `test_create_task_with_all_fields` - Verify Task(1, "Buy", True) works
2. `test_create_task_with_default_incomplete` - Verify is_complete defaults to False
3. `test_task_equality` - Verify two identical Tasks are equal
4. `test_task_inequality` - Verify different Tasks are not equal

**References**:
- Plan: "Unit Tests" table - "Task dataclass: Creation, default values, equality"
- Plan: "Files to Create (in order)" item 13

---

## Task 005: Implement TaskService Class - Core Storage

**Description**: Implement the TaskService class with in-memory task storage and initialization.

**Preconditions**:
- `src/services/__init__.py` exists
- `src/services/task_service.py` does not exist
- `src/models/task.py` exists (from Task 002)

**Expected Output**:
- `TaskService` class with:
  - `__init__()` method that initializes empty `_tasks` list and `_next_id=1`

**Artifacts**:
- Created: `src/services/task_service.py`

**Code Requirements**:
```python
from typing import List
from models.task import Task

class TaskService:
    """Handles all task operations with in-memory storage."""

    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id: int = 1
```

**References**:
- Plan: "Service Layer" section - `__init__()` method
- Plan: "In-memory data structures to store tasks"

**Testable By**:
- Running `python -c "from src.services.task_service import TaskService; s = TaskService(); print(len(s.get_all_tasks()))"`

---

## Task 006: Implement TaskService.add_task()

**Description**: Implement the add_task method that creates a new task with unique sequential ID.

**Preconditions**:
- `TaskService` class exists with `_tasks` and `_next_id` (from Task 005)

**Expected Output**:
- `add_task(title: str) -> Task` method that:
  - Creates Task with new sequential ID starting from 1
  - Sets title to provided value
  - Sets is_complete to False
  - Appends to `_tasks` list
  - Increments `_next_id`
  - Returns the created Task

**Artifacts**:
- Modified: `src/services/task_service.py`

**Code Requirements**:
```python
def add_task(self, title: str) -> Task:
    """Create a new task with unique ID."""
    task = Task(id=self._next_id, title=title, is_complete=False)
    self._tasks.append(task)
    self._next_id += 1
    return task
```

**References**:
- Spec: User Story 1 - "each task receives a unique ID"
- Spec: FR-001, FR-002
- Plan: "Service Layer" section - `add_task()` method

**Test Cases**:
1. `test_add_single_task` - Verify task created with ID 1
2. `test_add_multiple_tasks` - Verify sequential IDs (1, 2, 3)
3. `test_add_task_default_incomplete` - Verify is_complete is False

---

## Task 007: Implement TaskService.get_all_tasks()

**Description**: Implement the get_all_tasks method that returns all tasks.

**Preconditions**:
- `TaskService` class exists (from Task 005)

**Expected Output**:
- `get_all_tasks() -> List[Task]` method that:
  - Returns a copy of all tasks
  - Returns tasks in insertion order

**Artifacts**:
- Modified: `src/services/task_service.py`

**Code Requirements**:
```python
def get_all_tasks(self) -> List[Task]:
    """Return all tasks in insertion order."""
    return self._tasks.copy()
```

**References**:
- Spec: FR-003
- Plan: "Service Layer" section - `get_all_tasks()` method

**Test Cases**:
1. `test_get_empty_tasks` - Verify returns empty list when no tasks
2. `test_get_all_tasks` - Verify returns all added tasks
3. `test_get_returns_copy` - Verify returned list is a copy

---

## Task 008: Implement TaskService.get_task_by_id()

**Description**: Implement the get_task_by_id method for finding a specific task.

**Preconditions**:
- `TaskService` class exists (from Task 005)

**Expected Output**:
- `get_task_by_id(task_id: int) -> Optional[Task]` method that:
  - Searches for task with matching ID
  - Returns Task if found, None otherwise

**Artifacts**:
- Modified: `src/services/task_service.py`

**Code Requirements**:
```python
from typing import Optional

def get_task_by_id(self, task_id: int) -> Optional[Task]:
    """Find task by ID, returns None if not found."""
    for task in self._tasks:
        if task.id == task_id:
            return task
    return None
```

**References**:
- Plan: "Service Layer" section - `get_task_by_id()` method
- Spec: FR-008

**Test Cases**:
1. `test_get_existing_task` - Verify returns task when ID exists
2. `test_get_nonexistent_task` - Verify returns None when ID not found

---

## Task 009: Implement TaskService.update_task_title()

**Description**: Implement the update_task_title method for modifying task titles.

**Preconditions**:
- `TaskService` class exists (from Task 005)

**Expected Output**:
- `update_task_title(task_id: int, new_title: str) -> bool` method that:
  - Finds task by ID
  - Updates task's title to new_title
  - Returns True if successful, False if task not found

**Artifacts**:
- Modified: `src/services/task_service.py`

**Code Requirements**:
```python
def update_task_title(self, task_id: int, new_title: str) -> bool:
    """Update task title, return True if successful."""
    for task in self._tasks:
        if task.id == task_id:
            task.title = new_title
            return True
    return False
```

**References**:
- Spec: User Story 3 - "task's title is updated"
- Spec: FR-004
- Plan: "Service Layer" section - `update_task_title()` method

**Test Cases**:
1. `test_update_existing_task` - Verify returns True and updates title
2. `test_update_nonexistent_task` - Verify returns False when ID not found

---

## Task 010: Implement TaskService.delete_task()

**Description**: Implement the delete_task method for removing tasks.

**Preconditions**:
- `TaskService` class exists (from Task 005)

**Expected Output**:
- `delete_task(task_id: int) -> bool` method that:
  - Finds task by ID
  - Removes task from `_tasks` list
  - Returns True if successful, False if task not found

**Artifacts**:
- Modified: `src/services/task_service.py`

**Code Requirements**:
```python
def delete_task(self, task_id: int) -> bool:
    """Delete task by ID, return True if task was found and deleted."""
    for i, task in enumerate(self._tasks):
        if task.id == task_id:
            del self._tasks[i]
            return True
    return False
```

**References**:
- Spec: User Story 4 - "task is removed from the in-memory list"
- Spec: FR-005
- Plan: "Service Layer" section - `delete_task()` method

**Test Cases**:
1. `test_delete_existing_task` - Verify returns True and task removed
2. `test_delete_nonexistent_task` - Verify returns False when ID not found
3. `test_delete_preserves_other_tasks` - Verify other tasks remain

---

## Task 011: Implement TaskService.mark_complete()

**Description**: Implement the mark_complete method for marking tasks as done.

**Preconditions**:
- `TaskService` class exists (from Task 005)

**Expected Output**:
- `mark_complete(task_id: int) -> bool` method that:
  - Finds task by ID
  - Sets task's is_complete to True
  - Returns True if successful, False if task not found

**Artifacts**:
- Modified: `src/services/task_service.py`

**Code Requirements**:
```python
def mark_complete(self, task_id: int) -> bool:
    """Mark task as complete, return True if successful."""
    for task in self._tasks:
        if task.id == task_id:
            task.is_complete = True
            return True
    return False
```

**References**:
- Spec: User Story 5 - "task's status changes to complete"
- Spec: FR-006
- Plan: "Service Layer" section - `mark_complete()` method

**Test Cases**:
1. `test_mark_complete_existing` - Verify returns True and sets is_complete=True
2. `test_mark_complete_nonexistent` - Verify returns False when ID not found

---

## Task 012: Implement TaskService.mark_incomplete()

**Description**: Implement the mark_incomplete method for unmarked tasks.

**Preconditions**:
- `TaskService` class exists (from Task 005)

**Expected Output**:
- `mark_incomplete(task_id: int) -> bool` method that:
  - Finds task by ID
  - Sets task's is_complete to False
  - Returns True if successful, False if task not found

**Artifacts**:
- Modified: `src/services/task_service.py`

**Code Requirements**:
```python
def mark_incomplete(self, task_id: int) -> bool:
    """Mark task as incomplete, return True if successful."""
    for task in self._tasks:
        if task.id == task_id:
            task.is_complete = False
            return True
    return False
```

**References**:
- Spec: User Story 5 - "task's status changes to incomplete"
- Spec: FR-007
- Plan: "Service Layer" section - `mark_incomplete()` method

**Test Cases**:
1. `test_mark_incomplete_existing` - Verify returns True and sets is_complete=False
2. `test_mark_incomplete_nonexistent` - Verify returns False when ID not found

---

## Task 013: Write Unit Tests for TaskService

**Description**: Write comprehensive unit tests for all TaskService methods.

**Preconditions**:
- `src/services/task_service.py` is complete (Tasks 005-012)
- `tests/unit/test_task_service.py` does not exist

**Expected Output**:
- Test file with tests for all TaskService methods

**Artifacts**:
- Created: `tests/unit/test_task_service.py`

**Test Cases** (grouped by method):
- add_task: single task, multiple tasks, default incomplete
- get_all_tasks: empty, with tasks, returns copy
- get_task_by_id: existing, nonexistent
- update_task_title: existing, nonexistent
- delete_task: existing, nonexistent, preserves others
- mark_complete: existing, nonexistent
- mark_incomplete: existing, nonexistent

**References**:
- Plan: "Unit Tests" table - "TaskService: Each CRUD operation, edge cases, ID generation"
- Plan: "Files to Create (in order)" item 14

---

## Task 014: Implement CLI Menu - Base Class and Main Loop

**Description**: Implement the Menu class with main loop and menu display.

**Preconditions**:
- `src/cli/__init__.py` exists
- `src/cli/menu.py` does not exist
- `src/services/task_service.py` exists (from Task 005)

**Expected Output**:
- `Menu` class with:
  - `__init__(task_service: TaskService)` - Stores service via dependency injection
  - `run()` - Main menu loop that displays menu, gets input, routes to handlers
  - `_display_main_menu()` - Displays the 7-option menu
  - `_get_input(prompt: str) -> str` - Wrapper around input()

**Artifacts**:
- Created: `src/cli/menu.py`

**Code Requirements**:
```python
from services.task_service import TaskService

class Menu:
    """Handles all user interaction and menu display."""

    def __init__(self, task_service: TaskService):
        self._service = task_service

    def run(self):
        """Main menu loop."""
        while True:
            self._display_main_menu()
            choice = self._get_input("Enter your choice (1-7): ").strip()

            if choice == "1":
                self._handle_add_task()
            elif choice == "2":
                self._handle_view_tasks()
            elif choice == "3":
                self._handle_update_task()
            elif choice == "4":
                self._handle_delete_task()
            elif choice == "5":
                self._handle_mark_complete()
            elif choice == "6":
                self._handle_mark_incomplete()
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.\n")

    def _display_main_menu(self):
        """Display the main menu options."""
        print("=== Todo Application ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete")
        print("6. Mark Task Incomplete")
        print("7. Exit")
        print()

    def _get_input(self, prompt: str) -> str:
        """Get user input with the given prompt."""
        return input(prompt)
```

**References**:
- Spec: "CLI Interaction Design" - "Main Menu" section
- Plan: "CLI Layer" section - `run()` and `_display_main_menu()` methods
- Plan: "CLI Control Flow" - "Main Loop Flow" diagram

**Testable By**:
- Running `python -c "from src.cli.menu import Menu; from src.services.task_service import TaskService; m = Menu(TaskService())"` (then ctrl-c to exit)

---

## Task 015: Implement CLI Menu - Add Task Handler

**Description**: Implement the _handle_add_task method with input validation.

**Preconditions**:
- `Menu` class exists with `_service` (from Task 014)

**Expected Output**:
- `_handle_add_task()` method that:
  - Gets task title from user
  - Validates title is not empty/whitespace
  - Calls `service.add_task()` with valid title
  - Displays confirmation with new task ID
  - Handles empty title with error message

**Artifacts**:
- Modified: `src/cli/menu.py`

**Error Messages**:
- Empty title: "Error: Task title cannot be empty."

**References**:
- Spec: User Story 1 acceptance scenarios
- Spec: "Add Task Flow" section
- Plan: "Error Message Specifications" table

**Test Cases**:
1. Valid title input creates task and shows confirmation
2. Empty title shows error message
3. Whitespace-only title shows error message

---

## Task 016: Implement CLI Menu - View Tasks Handler

**Description**: Implement the _handle_view_tasks method with task list display.

**Preconditions**:
- `Menu` class exists with `_service` (from Task 014)
- `Task` model exists (from Task 002)

**Expected Output**:
- `_handle_view_tasks()` method that:
  - Calls `service.get_all_tasks()`
  - Displays empty list message if no tasks
  - Displays task table with ID, Status, Title columns
  - Shows summary: "Total: X tasks (Y complete, Z incomplete)"

**Artifacts**:
- Modified: `src/cli/menu.py`

**Display Format**:
```
ID | Status    | Title
---+-----------+------------------
1  | [ ]       | Buy groceries
2  | [x]       | Call mom
3  | [ ]       | Finish report

Total: 3 tasks (1 complete, 2 incomplete)
```

**References**:
- Spec: User Story 2 acceptance scenarios
- Spec: "View Tasks Flow" section
- Plan: "Task List Display Format" section

**Test Cases**:
1. Empty list shows "No tasks available" message
2. List with tasks shows formatted table
3. Summary counts complete/incomplete correctly

---

## Task 017: Implement CLI Menu - Update Task Handler

**Description**: Implement the _handle_update_task method with ID and title validation.

**Preconditions**:
- `Menu` class exists with `_service` (from Task 014)

**Expected Output**:
- `_handle_update_task()` method that:
  - Prompts for task ID
  - Validates ID is numeric
  - Calls `service.update_task_title()` with valid ID and title
  - Displays success or error messages

**Artifacts**:
- Modified: `src/cli/menu.py`

**Error Messages**:
- Invalid ID format: "Error: Please enter a valid number."
- Task not found: "Error: Task with ID {id} not found."
- Empty title: "Error: Task title cannot be empty."

**References**:
- Spec: User Story 3 acceptance scenarios
- Spec: "Update Task Flow" section
- Plan: "Error Message Specifications" table

**Test Cases**:
1. Valid ID and title updates task successfully
2. Non-numeric ID shows error
3. Non-existent ID shows task not found error
4. Empty new title shows error

---

## Task 018: Implement CLI Menu - Delete Task Handler

**Description**: Implement the _handle_delete_task method.

**Preconditions**:
- `Menu` class exists with `_service` (from Task 014)

**Expected Output**:
- `_handle_delete_task()` method that:
  - Prompts for task ID
  - Validates ID is numeric
  - Calls `service.delete_task()` with ID
  - Displays success or error messages

**Artifacts**:
- Modified: `src/cli/menu.py`

**Error Messages**:
- Invalid ID format: "Error: Please enter a valid number."
- Task not found: "Error: Task with ID {id} not found."
- Empty list: "Error: No tasks available."

**References**:
- Spec: User Story 4 acceptance scenarios
- Spec: "Delete Task Flow" section
- Plan: "Error Message Specifications" table

**Test Cases**:
1. Valid ID deletes task successfully
2. Non-numeric ID shows error
3. Non-existent ID shows task not found error

---

## Task 019: Implement CLI Menu - Mark Complete Handler

**Description**: Implement the _handle_mark_complete method.

**Preconditions**:
- `Menu` class exists with `_service` (from Task 014)

**Expected Output**:
- `_handle_mark_complete()` method that:
  - Prompts for task ID
  - Validates ID is numeric
  - Calls `service.mark_complete()` with ID
  - Displays success or error messages

**Artifacts**:
- Modified: `src/cli/menu.py`

**Error Messages**:
- Invalid ID format: "Error: Please enter a valid number."
- Task not found: "Error: Task with ID {id} not found."

**References**:
- Spec: User Story 5 acceptance scenarios
- Spec: "Mark Complete Flow" section
- Plan: "Error Message Specifications" table

**Test Cases**:
1. Valid ID marks task complete successfully
2. Non-numeric ID shows error
3. Non-existent ID shows task not found error

---

## Task 020: Implement CLI Menu - Mark Incomplete Handler

**Description**: Implement the _handle_mark_incomplete method.

**Preconditions**:
- `Menu` class exists with `_service` (from Task 014)

**Expected Output**:
- `_handle_mark_incomplete()` method that:
  - Prompts for task ID
  - Validates ID is numeric
  - Calls `service.mark_incomplete()` with ID
  - Displays success or error messages

**Artifacts**:
- Modified: `src/cli/menu.py`

**Error Messages**:
- Invalid ID format: "Error: Please enter a valid number."
- Task not found: "Error: Task with ID {id} not found."

**References**:
- Spec: User Story 5 acceptance scenarios
- Spec: "Mark Incomplete Flow" section
- Plan: "Error Message Specifications" table

**Test Cases**:
1. Valid ID marks task incomplete successfully
2. Non-numeric ID shows error
3. Non-existent ID shows task not found error

---

## Task 021: Create Application Entry Point

**Description**: Create the main entry point script that starts the application.

**Preconditions**:
- `todo.py` does not exist
- `src/services/task_service.py` exists (from Task 005)
- `src/cli/menu.py` exists (from Task 014)

**Expected Output**:
- `todo.py` file that:
  - Creates TaskService instance
  - Creates Menu instance with service
  - Calls menu.run()
  - Handles __main__ guard

**Artifacts**:
- Created: `todo.py`

**Code Requirements**:
```python
from services.task_service import TaskService
from cli.menu import Menu

def main():
    """Application entry point."""
    service = TaskService()
    menu = Menu(service)
    menu.run()

if __name__ == "__main__":
    main()
```

**References**:
- Plan: "Main Entry Point" section
- Plan: "Files to Create (in order)" item 8

**Testable By**:
- Running `python todo.py` (then type "7" to exit)

---

## Task 022: Create conftest.py

**Description**: Create pytest configuration with shared fixtures.

**Preconditions**:
- `tests/conftest.py` does not exist
- `src/services/task_service.py` exists (from Task 005)

**Expected Output**:
- `conftest.py` with fixtures for:
  - TaskService instance
  - Sample Task objects

**Artifacts**:
- Created: `tests/conftest.py`

**References**:
- Plan: "Test Structure" section
- Plan: "Files to Create (in order)" item 11

---

## Task 023: Create Integration Tests - Full Workflows

**Description**: Create integration tests for complete user workflows.

**Preconditions**:
- `tests/integration/test_workflows.py` does not exist
- All implementation tasks complete (001-021)

**Expected Output**:
- Integration test file covering:
  - Full add → view → update → delete flow
  - Mark complete → view → mark incomplete flow
  - Invalid ID operations error handling

**Artifacts**:
- Created: `tests/integration/test_workflows.py`

**Test Cases**:
1. `test_full_crud_workflow` - Add, view, update, delete tasks
2. `test_complete_incomplete_workflow` - Mark complete, view, mark incomplete
3. `test_invalid_operations` - All error paths

**References**:
- Plan: "Integration Tests" table
- Plan: "Files to Create (in order)" item 16

---

## Task 024: Run All Tests and Verify

**Description**: Run the full test suite and verify all tests pass.

**Preconditions**:
- All implementation complete (Tasks 001-023)
- pytest is installed

**Expected Output**:
- All unit and integration tests pass
- Test coverage includes all TaskService methods and Menu handlers

**Commands**:
```bash
pytest tests/ -v
```

**References**:
- Plan: "Test Command"
- Spec: "Definition of Done"

---

## Task Summary

| Task | Description | Status |
|------|-------------|--------|
| 001 | Create directory structure | pending |
| 002 | Implement Task dataclass | pending |
| 003 | Create requirements.txt | pending |
| 004 | Test Task dataclass | pending |
| 005 | TaskService core storage | pending |
| 006 | TaskService.add_task() | pending |
| 007 | TaskService.get_all_tasks() | pending |
| 008 | TaskService.get_task_by_id() | pending |
| 009 | TaskService.update_task_title() | pending |
| 010 | TaskService.delete_task() | pending |
| 011 | TaskService.mark_complete() | pending |
| 012 | TaskService.mark_incomplete() | pending |
| 013 | Test TaskService | pending |
| 014 | CLI menu base and loop | pending |
| 015 | CLI add task handler | pending |
| 016 | CLI view tasks handler | pending |
| 017 | CLI update task handler | pending |
| 018 | CLI delete task handler | pending |
| 019 | CLI mark complete handler | pending |
| 020 | CLI mark incomplete handler | pending |
| 021 | Application entry point | pending |
| 022 | Create conftest.py | pending |
| 023 | Integration tests | pending |
| 024 | Run all tests | pending |
