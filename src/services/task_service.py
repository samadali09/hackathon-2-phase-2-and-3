# [Spec]: specs/features/task-crud.md § All Features
# [Constitution]: constitution.md § Service Layer

"""
Task service layer for business logic and validation.

This module implements the business logic for task operations,
including input validation and coordination between storage and UI.
"""

from storage.memory_store import MemoryStore
from models.task import Task
from models.exceptions import InvalidTaskDataError, TaskNotFoundError
from typing import Optional


class TaskService:
    """
    Service layer for task operations.
    
    This class handles business logic, validation, and coordinates
    between the storage layer and the UI layer.
    
    Attributes:
        _store: MemoryStore instance for data persistence
    """
    
    def __init__(self, store: MemoryStore) -> None:
        """
        Initialize the task service.
        
        Args:
            store: MemoryStore instance for task storage
        """
        self._store = store
    
    def _validate_title(self, title: str) -> None:
        """
        Validate task title.
        
        Args:
            title: Task title to validate
        
        Raises:
            InvalidTaskDataError: If validation fails
        """
        if not title or len(title.strip()) == 0:
            raise InvalidTaskDataError("Title cannot be empty")
        
        if len(title) > 200:
            raise InvalidTaskDataError("Title cannot exceed 200 characters")
    
    def _validate_description(self, description: str) -> None:
        """
        Validate task description.
        
        Args:
            description: Task description to validate
        
        Raises:
            InvalidTaskDataError: If validation fails
        """
        if len(description) > 1000:
            raise InvalidTaskDataError("Description cannot exceed 1000 characters")
    
    def add_task(self, title: str, description: str = "") -> Task:
        """
        Create a new task with validation.
        
        Args:
            title: Task title (required, 1-200 characters)
            description: Task description (optional, max 1000 characters)
        
        Returns:
            The newly created Task object
        
        Raises:
            InvalidTaskDataError: If validation fails
        
        Example:
            >>> service = TaskService(MemoryStore())
            >>> task = service.add_task("Buy groceries", "Milk, eggs, bread")
            >>> print(task.id)
            1
        """
        # Validate inputs
        self._validate_title(title)
        self._validate_description(description)
        
        # Strip whitespace
        title = title.strip()
        description = description.strip()
        
        # Create task
        return self._store.create(title, description)
    
    def get_all_tasks(self) -> list[Task]:
        """
        Retrieve all tasks.
        
        Returns:
            List of all Task objects (may be empty)
        
        Example:
            >>> service = TaskService(MemoryStore())
            >>> tasks = service.get_all_tasks()
            >>> len(tasks)
            0
        """
        return self._store.get_all()
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by ID.
        
        Args:
            task_id: The task ID to retrieve
        
        Returns:
            Task object if found, None otherwise
        
        Example:
            >>> service = TaskService(MemoryStore())
            >>> task = service.get_task(1)
            >>> task is None
            True
        """
        return self._store.get(task_id)
    
    def update_task(self, task_id: int, title: str, description: str) -> Task:
        """
        Update an existing task with validation.
        
        Args:
            task_id: The task ID to update
            title: New title (required, 1-200 characters)
            description: New description (optional, max 1000 characters)
        
        Returns:
            The updated Task object
        
        Raises:
            TaskNotFoundError: If task doesn't exist
            InvalidTaskDataError: If validation fails
        
        Example:
            >>> service = TaskService(MemoryStore())
            >>> task = service.add_task("Buy groceries", "Milk, eggs")
            >>> updated = service.update_task(task.id, "Buy groceries and fruits", "Milk, eggs, apples")
            >>> updated.title
            'Buy groceries and fruits'
        """
        # Validate inputs
        self._validate_title(title)
        self._validate_description(description)
        
        # Strip whitespace
        title = title.strip()
        description = description.strip()
        
        # Update task
        return self._store.update(task_id, title, description)
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.
        
        Args:
            task_id: The task ID to delete
        
        Returns:
            True if deleted, False if not found
        
        Example:
            >>> service = TaskService(MemoryStore())
            >>> task = service.add_task("Buy groceries", "")
            >>> service.delete_task(task.id)
            True
            >>> service.delete_task(999)
            False
        """
        return self._store.delete(task_id)
    
    def toggle_completion(self, task_id: int) -> Task:
        """
        Toggle task completion status.
        
        Args:
            task_id: The task ID to toggle
        
        Returns:
            The updated Task object
        
        Raises:
            TaskNotFoundError: If task doesn't exist
        
        Example:
            >>> service = TaskService(MemoryStore())
            >>> task = service.add_task("Buy groceries", "")
            >>> task.completed
            False
            >>> toggled = service.toggle_completion(task.id)
            >>> toggled.completed
            True
        """
        return self._store.toggle_completion(task_id)
