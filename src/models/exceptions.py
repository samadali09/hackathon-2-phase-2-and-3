# [Spec]: specs/data-model.md § Custom Exceptions
# [Constitution]: constitution.md § Error Handling

"""
Custom exceptions for the Todo Console App.

This module defines application-specific exceptions for error handling.
"""


class TaskNotFoundError(Exception):
    """
    Raised when a task ID doesn't exist in storage.
    
    This exception is raised during operations that require an existing task
    (update, delete, toggle completion) when the specified task ID is not found.
    
    Example:
        >>> raise TaskNotFoundError("Task 5 not found")
    """
    pass


class InvalidTaskDataError(Exception):
    """
    Raised when task data fails validation.
    
    This exception is raised when user input doesn't meet validation requirements,
    such as empty titles, titles/descriptions exceeding length limits, etc.
    
    Example:
        >>> raise InvalidTaskDataError("Title cannot be empty")
    """
    pass
