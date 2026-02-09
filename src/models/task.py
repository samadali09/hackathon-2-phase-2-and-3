# [Spec]: specs/data-model.md § Task Model
# [Constitution]: constitution.md § Data Model Standards

"""
Task data model for the Todo Console App.

This module defines the Task dataclass representing a single todo item.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    """
    Represents a single todo task.
    
    Attributes:
        id: Unique identifier (auto-generated, positive integer)
        title: Task title (required, 1-200 characters)
        description: Detailed description (optional, max 1000 characters)
        completed: Completion status (True = completed, False = pending)
        created_at: Creation timestamp (UTC, auto-set)
        updated_at: Last modification timestamp (UTC, auto-managed)
    
    Example:
        >>> task = Task(
        ...     id=1,
        ...     title="Buy groceries",
        ...     description="Milk, eggs, bread",
        ...     completed=False,
        ...     created_at=datetime.utcnow(),
        ...     updated_at=datetime.utcnow()
        ... )
    """
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime
