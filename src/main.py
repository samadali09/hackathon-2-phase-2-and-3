# [Spec]: specs/overview.md § Project Structure
# [Constitution]: constitution.md § Main Entry Point

"""
Todo Console App - Main Entry Point

This is Phase I of Hackathon II: A spec-driven todo console application
with in-memory storage.

Usage:
    python src/main.py
"""

import sys
from pathlib import Path

# Add src directory to Python path for imports
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from storage.memory_store import MemoryStore
from services.task_service import TaskService
from ui.console_ui import ConsoleUI


def main() -> None:
    """
    Main application entry point.
    
    Initializes the storage, service, and UI layers, then runs the application.
    """
    # Initialize layers
    store = MemoryStore()
    service = TaskService(store)
    ui = ConsoleUI(service)
    
    # Run application
    ui.run()


if __name__ == "__main__":
    main()
