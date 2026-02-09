# [Spec]: specs/data-model.md § In-Memory Storage Design
# [Constitution]: constitution.md § Storage Layer

"""
In-memory storage for tasks.

This module provides a dictionary-based in-memory storage implementation
for managing Task objects during the application session.
"""

from datetime import datetime
from typing import Optional

from models.task import Task
from models.exceptions import TaskNotFoundError


class MemoryStore:
    """
    In-memory storage for tasks using dictionary.
    
    This class manages task storage in memory with auto-incrementing IDs.
    Data is lost when the application exits (expected behavior for Phase I).
    
    Attributes:
        _tasks: Dictionary mapping task IDs to Task objects
        _next_id: Auto-increment counter for generating unique task IDs
    """
    
    def __init__(self) -> None:
        """Initialize empty storage with ID counter starting at 1."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
    
    def _generate_id(self) -> int:
        """
        Generate next unique task ID.
        
        Returns:
            Next available ID (auto-incremented)
        
        Note:
            IDs are never reused, even after deletion.
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id
    
    def create(self, title: str, description: str = "") -> Task:
        """
        Create a new task and store it.
        
        Args:
            title: Task title (already validated, trimmed)
            description: Task description (already validated, trimmed)
        
        Returns:
            The newly created Task object
        
        Note:
            Validation should be performed in the service layer before calling this method.
        """
        task_id = self._generate_id()
        now = datetime.utcnow()
        
        task = Task(
            id=task_id,
            title=title,
            description=description,
            completed=False,
            created_at=now,
            updated_at=now
        )
        
        self._tasks[task_id] = task
        return task
    
    def get(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by ID.
        
        Args:
            task_id: The task ID to retrieve
        
        Returns:
            Task object if found, None otherwise
        """
        return self._tasks.get(task_id)
    
    def get_all(self) -> list[Task]:
        """
        Retrieve all tasks.
        
        Returns:
            List of all Task objects (may be empty)
        
        Note:
            Tasks are returned in arbitrary order (dictionary iteration order).
        """
        return list(self._tasks.values())
    
    def update(self, task_id: int, title: str, description: str) -> Task:
        """
        Update an existing task.
        
        Args:
            task_id: The task ID to update
            title: New title (already validated, trimmed)
            description: New description (already validated, trimmed)
        
        Returns:
            The updated Task object
        
        Raises:
            TaskNotFoundError: If task doesn't exist
        
        Note:
            Only title and description are updated. Completion status,
            created_at, and id remain unchanged. updated_at is set to current time.
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        
        # Create updated task (following immutable pattern)
        updated_task = Task(
            id=task.id,
            title=title,
            description=description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=datetime.utcnow()
        )
        
        self._tasks[task_id] = updated_task
        return updated_task
    
    def delete(self, task_id: int) -> bool:
        """
        Delete a task by ID.
        
        Args:
            task_id: The task ID to delete
        
        Returns:
            True if deleted, False if not found
        
        Note:
            Deleted task IDs are never reused.
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
    
    def toggle_completion(self, task_id: int) -> Task:
        """
        Toggle task completion status.
        
        Args:
            task_id: The task ID to toggle
        
        Returns:
            The updated Task object
        
        Raises:
            TaskNotFoundError: If task doesn't exist
        
        Note:
            This method flips the completed status (True → False, False → True)
            and updates the updated_at timestamp.
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        
        updated_task = Task(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=not task.completed,  # Toggle
            created_at=task.created_at,
            updated_at=datetime.utcnow()
        )
        
        self._tasks[task_id] = updated_task
        return updated_task
