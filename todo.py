"""Todo Application - Main entry point.

A simple console-based todo list application.
Run with: python todo.py
"""

from src.services.task_service import TaskService
from src.cli.menu import Menu


def main():
    """Application entry point."""
    service = TaskService()
    menu = Menu(service)
    menu.run()


if __name__ == "__main__":
    main()
