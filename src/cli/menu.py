"""CLI Menu for the Todo Application.

Provides a menu-driven interface for managing tasks.
"""

from src.services.task_service import TaskService
from src.models.task import Task


class Menu:
    """Handles all user interaction and menu display.

    Args:
        task_service: The TaskService instance for task operations.
    """

    def __init__(self, task_service: TaskService):
        """Initialize the Menu with a TaskService instance."""
        self._service = task_service

    def run(self):
        """Run the main menu loop."""
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
        """Get user input with the given prompt.

        Args:
            prompt: The prompt to display to the user.

        Returns:
            The user's input string.
        """
        return input(prompt)

    def _handle_add_task(self):
        """Handle the Add Task menu option."""
        print("\n=== Add Task ===")
        title = self._get_input("Enter task title: ").strip()

        if not title:
            print("Error: Task title cannot be empty.\n")
            return

        task = self._service.add_task(title)
        print(f"Task added successfully! (ID: {task.id})\n")

    def _handle_view_tasks(self):
        """Handle the View Tasks menu option."""
        print("\n=== Task List ===")

        tasks = self._service.get_all_tasks()

        if not tasks:
            print("No tasks available.\n")
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
        print(f"Total: {len(tasks)} tasks ({complete_count} complete, {incomplete_count} incomplete)\n")

    def _handle_update_task(self):
        """Handle the Update Task menu option."""
        print("\n=== Update Task ===")

        if self._service.task_count() == 0:
            print("Error: No tasks available.\n")
            return

        id_str = self._get_input("Enter task ID: ").strip()

        if not id_str.isdigit():
            print("Error: Please enter a valid number.\n")
            return

        task_id = int(id_str)

        if self._service.get_task_by_id(task_id) is None:
            print(f"Error: Task with ID {task_id} not found.\n")
            return

        new_title = self._get_input("Enter new title: ").strip()

        if not new_title:
            print("Error: Task title cannot be empty.\n")
            return

        if self._service.update_task_title(task_id, new_title):
            print("Task updated successfully!\n")
        else:
            print(f"Error: Task with ID {task_id} not found.\n")

    def _handle_delete_task(self):
        """Handle the Delete Task menu option."""
        print("\n=== Delete Task ===")

        if self._service.task_count() == 0:
            print("Error: No tasks available.\n")
            return

        id_str = self._get_input("Enter task ID: ").strip()

        if not id_str.isdigit():
            print("Error: Please enter a valid number.\n")
            return

        task_id = int(id_str)

        if self._service.get_task_by_id(task_id) is None:
            print(f"Error: Task with ID {task_id} not found.\n")
            return

        if self._service.delete_task(task_id):
            print("Task deleted successfully!\n")
        else:
            print(f"Error: Task with ID {task_id} not found.\n")

    def _handle_mark_complete(self):
        """Handle the Mark Task Complete menu option."""
        print("\n=== Mark Task Complete ===")

        if self._service.task_count() == 0:
            print("Error: No tasks available.\n")
            return

        id_str = self._get_input("Enter task ID: ").strip()

        if not id_str.isdigit():
            print("Error: Please enter a valid number.\n")
            return

        task_id = int(id_str)

        if self._service.get_task_by_id(task_id) is None:
            print(f"Error: Task with ID {task_id} not found.\n")
            return

        if self._service.mark_complete(task_id):
            print("Task marked as complete!\n")
        else:
            print(f"Error: Task with ID {task_id} not found.\n")

    def _handle_mark_incomplete(self):
        """Handle the Mark Task Incomplete menu option."""
        print("\n=== Mark Task Incomplete ===")

        if self._service.task_count() == 0:
            print("Error: No tasks available.\n")
            return

        id_str = self._get_input("Enter task ID: ").strip()

        if not id_str.isdigit():
            print("Error: Please enter a valid number.\n")
            return

        task_id = int(id_str)

        if self._service.get_task_by_id(task_id) is None:
            print(f"Error: Task with ID {task_id} not found.\n")
            return

        if self._service.mark_incomplete(task_id):
            print("Task marked as incomplete!\n")
        else:
            print(f"Error: Task with ID {task_id} not found.\n")
