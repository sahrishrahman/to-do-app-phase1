# Implementation Plan: Phase I - Basic In-Memory Todo Application

**Branch**: `phase-i-basic-todo`
**Date**: 2025-12-25
**Spec**: `specs/phase-i-basic-todo/spec.md`
**Constitution Version**: 1.0.0

## Summary

This plan describes HOW to implement the Phase I in-memory todo console application. The application will be a single Python program that provides a menu-driven CLI for managing tasks. Tasks are stored in memory using a simple list. No databases, files, or external dependencies are used.

## Technical Context

| Aspect | Value |
|--------|-------|
| **Language/Version** | Python 3.11+ |
| **Primary Dependencies** | Standard library only (no external packages) |
| **Storage** | In-memory list (no database, no files) |
| **Testing** | pytest (standard library unittest also acceptable) |
| **Target Platform** | Terminal/Console (cross-platform: Windows, Linux, macOS) |
| **Project Type** | Single Python script |
| **Performance Goals** | <100ms response time for all operations |
| **Constraints** | No persistence, single user, keyboard-only input |
| **Scale/Scope** | Single session, in-memory only |

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | PASS | Following Spec → Plan → Tasks → Implementation flow |
| II. Human-Authorship Prohibition | PASS | Plan created for human approval before implementation |
| III. No Feature Invention | PASS | Plan derived strictly from approved specification |
| IV. Phase Isolation | PASS | No Phase II-V concepts included |
| V. Refinement at Spec Level | PASS | Plan clarifies technical approach without changing requirements |
| A. Clean Architecture | PASS | Separation of concerns planned (model, service, CLI) |
| B. Stateless Services | N/A | Single-user console app, no services |
| C. Separation of Concerns | PASS | Data layer separate from presentation layer |
| D. Cloud-Native Readiness | N/A | Phase I is local console app only |

## Project Structure

### Source Code Structure

```
todo-app/
├── todo.py                 # Main entry point
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py         # Task dataclass/entity
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py # Business logic for task operations
│   └── cli/
│       ├── __init__.py
│       └── menu.py         # CLI interface, menu display, user input
└── tests/
    ├── __init__.py
    ├── unit/
    │   ├── test_task.py
    │   └── test_task_service.py
    └── test_todo.py        # Integration tests
```

### Structure Decision

The project uses a three-layer architecture:
1. **models/** - Data entity (Task dataclass)
2. **services/** - Business logic (TaskService class)
3. **cli/** - User interface (Menu class, main loop)

This separation aligns with the constitution's clean architecture principle and facilitates future migration to FastAPI in Phase II.

## Technical Design

### 1. Data Model Layer (`src/models/task.py`)

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    """Represents a single todo task."""
    id: int
    title: str
    is_complete: bool = False
```

**Design Rationale:**
- Uses `@dataclass` for clean representation and automatic `__eq__`, `__hash__`
- `id` is read-only (set by service, never modified)
- `is_complete` defaults to `False` for new tasks

### 2. Service Layer (`src/services/task_service.py`)

```python
from typing import List, Optional
from models.task import Task

class TaskService:
    """Handles all task operations with in-memory storage."""

    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str) -> Task:
        """Create a new task with unique ID."""
        task = Task(id=self._next_id, title=title, is_complete=False)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks in insertion order."""
        return self._tasks.copy()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Find task by ID, returns None if not found."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task_title(self int, new_title, task_id:: str) -> bool:
        """Update task title, return True if successful."""
        for task in self._tasks:
            if task.id == task_id:
                task.title = new_title
                return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID, return True if task was found and deleted."""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                return True
        return False

    def mark_complete(self, task_id: int) -> bool:
        """Mark task as complete, return True if successful."""
        for task in self._tasks:
            if task.id == task_id:
                task.is_complete = True
                return True
        return False

    def mark_incomplete(self, task_id: int) -> bool:
        """Mark task as incomplete, return True if successful."""
        for task in self._tasks:
            if task.id == task_id:
                task.is_complete = False
                return True
        return False
```

**Design Rationale:**
- All operations return success/failure indicators for error handling
- `_tasks` is private to prevent external modification
- `get_all_tasks()` returns a copy to prevent external mutation
- Sequential ID generation ensures uniqueness

### 3. CLI Layer (`src/cli/menu.py`)

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

    # Individual menu handlers with error handling...
```

**Design Rationale:**
- Dependency injection of `TaskService` for testability
- Separate methods for each menu option
- Clear separation between display logic and input handling

### 4. Main Entry Point (`todo.py`)

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

## ID Generation Strategy

**Approach:** Sequential integer IDs starting from 1

| Aspect | Value |
|--------|-------|
| **Starting Value** | 1 |
| **Increment** | +1 per task |
| **Uniqueness** | Guaranteed by sequential generation |
| **Reuse** | IDs are NOT reused after deletion (deleted task ID is lost) |

**Rationale:**
- Simple and predictable
- Matches spec requirement for unique IDs
- No collision handling needed
- Deleted task IDs are not reused (acceptable per spec)

## CLI Control Flow

### Main Loop Flow

```
┌─────────────────────────────────────┐
│           Start Application         │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│         Display Main Menu           │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│        Get User Input               │
│    (1-7, or show error)            │
└─────────────────┬───────────────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
  Choice 1     Choice 7     Other
    │             │             │
    ▼             ▼             ▼
  Add Task     Exit Loop   Show Error
    │             │          Back to Menu
    └─────────────┴─────────────┘
                  ▼
         Return to Menu Display
```

### Input Validation Flow

```
User Input
    │
    ▼
┌───────────────────────────────┐
│ Is input a digit 1-7?        │
└─────────────┬─────────────────┘
              │
     ┌────────┴────────┐
     ▼                 ▼
    YES                NO
     │                 │
     ▼                 ▼
 Execute          Show Error
 Selected         "Invalid choice"
 Operation        Return to Menu
     │
     ▼
 Continue or Exit
```

## Error Handling Strategy

### Error Types and Handling

| Error Type | Example | Handling Approach |
|------------|---------|-------------------|
| Invalid menu choice | "9", "abc" | Print error, show menu again |
| Non-numeric task ID | "abc", "1.5" | Print "Please enter a valid number", reprompt |
| Task ID not found | ID 99 when only 1-5 exist | Print "Task with ID {id} not found", return to menu |
| Empty title | "" or "   " | Print "Task title cannot be empty", reprompt |
| Empty task list | User selects delete when no tasks | Print "No tasks available", return to menu |

### Error Message Specifications (from Spec)

| Error Condition | Message |
|-----------------|---------|
| Invalid menu choice | "Invalid choice. Please enter a number between 1 and 7." |
| Task not found | "Error: Task with ID {id} not found." |
| Empty title | "Error: Task title cannot be empty." |
| Invalid ID format | "Error: Please enter a valid number." |
| Empty list operations | "Error: No tasks available." |

### Reprompt Pattern

For operations requiring valid input (task ID, title):
- On invalid input, show error message
- Return to previous menu (do not auto-reprompt)
- User can navigate back via menu

## Task List Display Format

From the spec, the task list display format is:

```
ID | Status    | Title
---+-----------+------------------
1  | [ ]       | Buy groceries
2  | [x]       | Call mom
3  | [ ]       | Finish report

Total: 3 tasks (1 complete, 2 incomplete)
```

**Display Implementation:**

```python
def _display_tasks(self, tasks: List[Task]):
    if not tasks:
        print("No tasks available.")
        return

    print("ID | Status    | Title")
    print("---+-----------+------------------")

    complete_count = 0
    for task in tasks:
        status = "[x]" if task.is_complete else "[ ]"
        print(f"{task.id:<2} | {status}     | {task.title}")
        if task.is_complete:
            complete_count += 1

    incomplete_count = len(tasks) - complete_count
    print()
    print(f"Total: {len(tasks)} tasks ({complete_count} complete, {incomplete_count} incomplete)")
```

## Testing Strategy

### Unit Tests

| Component | Tests |
|-----------|-------|
| Task dataclass | Creation, default values, equality |
| TaskService | Each CRUD operation, edge cases, ID generation |
| Menu | Input parsing, menu display |

### Integration Tests

| Scenario | Coverage |
|----------|----------|
| Full add → view → update → delete flow | All operations |
| Mark complete → view → mark incomplete | Status toggling |
| Invalid ID operations | Error handling |

### Test Structure

```
tests/
├── __init__.py
├── conftest.py           # Shared fixtures
├── unit/
│   ├── __init__.py
│   ├── test_task.py      # Task dataclass tests
│   └── test_task_service.py  # Service layer tests
└── integration/
    ├── __init__.py
    └── test_workflows.py # Full user journey tests
```

## Complexity Tracking

No Constitution violations in this implementation. The simple single-script nature is appropriate for Phase I scope.

| Aspect | Decision | Justification |
|--------|----------|---------------|
| Directory structure | `src/` with subpackages | Clean separation of concerns, Phase II migration path |
| Dataclass usage | Standard library `@dataclass` | No external dependencies, clean code |
| Service class | Separate from CLI | Testability, future API migration |
| Testing | pytest | Standard Python testing |

## Implementation Notes

### Files to Create (in order)

1. `src/__init__.py`
2. `src/models/__init__.py`
3. `src/models/task.py`
4. `src/services/__init__.py`
5. `src/services/task_service.py`
6. `src/cli/__init__.py`
7. `src/cli/menu.py`
8. `todo.py`
9. `requirements.txt` (for testing, pytest only)
10. `tests/__init__.py`
11. `tests/conftest.py`
12. `tests/unit/__init__.py`
13. `tests/unit/test_task.py`
14. `tests/unit/test_task_service.py`
15. `tests/integration/__init__.py`
16. `tests/integration/test_workflows.py`

### Run Command

```bash
python todo.py
```

### Test Command

```bash
pytest tests/ -v
```

## Acceptance Criteria Verification

This plan enables implementation that satisfies all Phase I acceptance scenarios:

| Scenario | Implementation |
|----------|----------------|
| Add valid task | `TaskService.add_task()` → `Menu._handle_add_task()` |
| Add empty title rejected | Input validation in menu handler |
| View empty list | `Menu._handle_view_tasks()` shows "No tasks available" |
| View tasks with status | Table display with `[ ]`/`[x]` status |
| Update by ID | `TaskService.update_task_title()` |
| Delete by ID | `TaskService.delete_task()` |
| Mark complete/incomplete | `TaskService.mark_complete()` / `mark_incomplete()` |
| Invalid ID handling | Service returns False, menu shows error |
