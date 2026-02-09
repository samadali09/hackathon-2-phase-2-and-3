# [Spec]: specs/features/task-crud.md § Console Menu Specification
# [Constitution]: constitution.md § UI Layer

"""
Console user interface for the Todo App.

This module handles all user interaction, including menu display,
input collection, and output formatting.
"""

from services.task_service import TaskService
from models.task import Task
from models.exceptions import InvalidTaskDataError, TaskNotFoundError


class ConsoleUI:
    """
    Console interface for user interaction.
    
    This class manages the console menu, user input, and task display.
    
    Attributes:
        _service: TaskService instance for business operations
    """
    
    def __init__(self, service: TaskService) -> None:
        """
        Initialize the console UI.
        
        Args:
            service: TaskService instance for task operations
        """
        self._service = service
    
    def _clear_screen(self) -> None:
        """Clear the console screen (optional, simple implementation)."""
        print("\n" * 2)
    
    def _pause(self) -> None:
        """Pause and wait for user to press Enter."""
        input("\nPress Enter to continue...")
    
    def _display_menu(self) -> None:
        """Display the main menu."""
        print("\n=== Todo App ===")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete/Incomplete")
        print("6. Exit")
        print()
    
    def _format_task(self, task: Task) -> str:
        """
        Format a task for display.
        
        Args:
            task: Task object to format
        
        Returns:
            Formatted string representation of the task
        """
        status = "Completed" if task.completed else "Pending"
        created = task.created_at.strftime("%Y-%m-%d %H:%M:%S")
        updated = task.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""ID: {task.id}
Title: {task.title}
Description: {task.description}
Status: {status}
Created: {created}
Updated: {updated}
---"""
    
    def _get_int_input(self, prompt: str) -> int:
        """
        Get integer input from user with validation.
        
        Args:
            prompt: Prompt message to display
        
        Returns:
            Valid integer input
        
        Note:
            Keeps prompting until valid integer is entered.
        """
        while True:
            try:
                value = input(prompt)
                return int(value)
            except ValueError:
                print("Error: Please enter a valid task ID (number)")
    
    def add_task_ui(self) -> None:
        """Handle Add Task feature UI."""
        print("\n=== Add Task ===\n")
        
        # Get title with validation
        while True:
            title = input("Enter task title: ")
            try:
                # Get description
                description = input("Enter task description (optional, press Enter to skip): ")
                
                # Create task
                task = self._service.add_task(title, description)
                print(f"\nTask created successfully! (ID: {task.id})")
                break
            except InvalidTaskDataError as e:
                print(f"\nError: {e}")
                if "Title" in str(e):
                    continue  # Re-prompt for title
                else:
                    break  # Description error, restart
        
        self._pause()
    
    def view_tasks_ui(self) -> None:
        """Handle View All Tasks feature UI."""
        print("\n=== All Tasks ===\n")
        
        tasks = self._service.get_all_tasks()
        
        if not tasks:
            print("No tasks found. Add a task to get started!")
        else:
            for task in tasks:
                print(self._format_task(task))
        
        self._pause()
    
    def update_task_ui(self) -> None:
        """Handle Update Task feature UI."""
        print("\n=== Update Task ===\n")
        
        task_id = self._get_int_input("Enter task ID to update: ")
        
        # Check if task exists
        task = self._service.get_task(task_id)
        if task is None:
            print(f"\nError: Task {task_id} not found")
            self._pause()
            return
        
        # Show current values
        print(f"\nCurrent Task:")
        print(f"Title: {task.title}")
        print(f"Description: {task.description}\n")
        
        # Get new values with validation
        while True:
            title = input("Enter new title: ")
            description = input("Enter new description (press Enter to keep current): ")
            
            # Use current description if user pressed Enter
            if not description.strip():
                description = task.description
            
            try:
                updated_task = self._service.update_task(task_id, title, description)
                print(f"\nTask {task_id} updated successfully!")
                break
            except InvalidTaskDataError as e:
                print(f"\nError: {e}")
                continue
            except TaskNotFoundError as e:
                print(f"\nError: {e}")
                break
        
        self._pause()
    
    def delete_task_ui(self) -> None:
        """Handle Delete Task feature UI."""
        print("\n=== Delete Task ===\n")
        
        task_id = self._get_int_input("Enter task ID to delete: ")
        
        # Check if task exists
        task = self._service.get_task(task_id)
        if task is None:
            print(f"\nError: Task {task_id} not found")
            self._pause()
            return
        
        # Show task to be deleted
        print(f"\nTask to delete:")
        print(self._format_task(task))
        
        # Confirm deletion
        confirmation = input("\nAre you sure you want to delete this task? (y/n): ")
        
        if confirmation.lower() == 'y':
            self._service.delete_task(task_id)
            print(f"\nTask {task_id} deleted successfully!")
        else:
            print("\nDeletion cancelled.")
        
        self._pause()
    
    def toggle_completion_ui(self) -> None:
        """Handle Mark Task Complete/Incomplete feature UI."""
        print("\n=== Mark Task Complete/Incomplete ===\n")
        
        task_id = self._get_int_input("Enter task ID to toggle completion: ")
        
        # Check if task exists
        task = self._service.get_task(task_id)
        if task is None:
            print(f"\nError: Task {task_id} not found")
            self._pause()
            return
        
        # Show current status
        current_status = "Completed" if task.completed else "Pending"
        print(f"\nCurrent Status: {current_status}")
        
        try:
            # Toggle completion
            updated_task = self._service.toggle_completion(task_id)
            new_status = "completed" if updated_task.completed else "incomplete"
            print(f"\nTask {task_id} marked as {new_status}!")
        except TaskNotFoundError as e:
            print(f"\nError: {e}")
        
        self._pause()
    
    def run(self) -> None:
        """
        Run the main application loop.
        
        This method displays the menu and handles user choices until exit.
        """
        while True:
            self._display_menu()
            
            try:
                choice = input("Enter your choice: ")
                
                if choice == "1":
                    self.add_task_ui()
                elif choice == "2":
                    self.view_tasks_ui()
                elif choice == "3":
                    self.update_task_ui()
                elif choice == "4":
                    self.delete_task_ui()
                elif choice == "5":
                    self.toggle_completion_ui()
                elif choice == "6":
                    print("\nThank you for using Todo App. Goodbye!")
                    break
                else:
                    print("\nInvalid choice. Please enter a number between 1 and 6.")
                    self._pause()
            except KeyboardInterrupt:
                print("\n\nThank you for using Todo App. Goodbye!")
                break
            except Exception as e:
                print(f"\nAn unexpected error occurred: {e}")
                self._pause()
