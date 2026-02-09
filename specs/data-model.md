# Data Model Specification

## Overview

This document defines the data structures and storage design for the Todo Console App (Phase I).

---

## Task Model

### Entity Definition

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    """
    Represents a single todo task.
    
    Attributes:
        id: Unique identifier (auto-generated)
        title: Task title (required)
        description: Detailed description (optional)
        completed: Completion status
        created_at: Creation timestamp
        updated_at: Last modification timestamp
    """
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime
```

### Field Specifications

#### id: int
- **Type**: Positive integer
- **Generation**: Auto-incremented (1, 2, 3, ...)
- **Uniqueness**: Must be unique across all tasks
- **Immutability**: Never changes after creation
- **Range**: 1 to 2,147,483,647 (max int)

#### title: str
- **Type**: String
- **Required**: Yes
- **Validation**:
  - Minimum length: 1 character (after stripping whitespace)
  - Maximum length: 200 characters
  - Cannot be empty or whitespace-only
- **Examples**:
  - ✅ "Buy groceries"
  - ✅ "Call mom"
  - ❌ "" (empty)
  - ❌ "   " (whitespace only)

#### description: str
- **Type**: String
- **Required**: No (can be empty)
- **Validation**:
  - Maximum length: 1000 characters
  - Can be empty string
- **Default**: Empty string ("")
- **Examples**:
  - ✅ "Milk, eggs, bread, butter"
  - ✅ "" (empty is valid)
  - ✅ "Remember to check expiration dates"

#### completed: bool
- **Type**: Boolean
- **Required**: Yes
- **Default**: False (new tasks are incomplete)
- **Values**:
  - `True`: Task is completed
  - `False`: Task is pending
- **Mutability**: Can be toggled multiple times

#### created_at: datetime
- **Type**: datetime object
- **Required**: Yes
- **Generation**: Auto-set on task creation
- **Timezone**: UTC
- **Immutability**: Never changes after creation
- **Format**: ISO 8601 (for display)
- **Example**: `2025-12-05T14:30:00Z`

#### updated_at: datetime
- **Type**: datetime object
- **Required**: Yes
- **Generation**: Auto-set on creation and updates
- **Timezone**: UTC
- **Mutability**: Updated on every modification
- **Format**: ISO 8601 (for display)
- **Example**: `2025-12-05T15:45:00Z`

---

## Storage Design

### In-Memory Storage Structure

```python
class MemoryStore:
    """In-memory storage for tasks using dictionary."""
    
    def __init__(self):
        self._tasks: dict[int, Task] = {}  # Task ID -> Task object
        self._next_id: int = 1              # Auto-increment counter
```

### Storage Characteristics

#### Data Structure
- **Type**: Python dictionary (`dict[int, Task]`)
- **Key**: Task ID (integer)
- **Value**: Task object
- **Advantages**:
  - O(1) lookup by ID
  - O(1) insertion
  - O(1) deletion
  - Simple iteration for listing

#### ID Generation Strategy

```python
def _generate_id(self) -> int:
    """
    Generate next unique task ID.
    
    Returns:
        Next available ID (auto-incremented)
    """
    current_id = self._next_id
    self._next_id += 1
    return current_id
```

**Rules**:
- Start at 1
- Increment by 1 for each new task
- Never reuse IDs (even after deletion)
- Thread-safe not required (single-threaded app)

#### Persistence
- **Lifetime**: Application session only
- **Behavior**: Data lost on exit
- **Rationale**: Phase I requirement (in-memory only)
- **Future**: Will be replaced with database in Phase II

---

## CRUD Operations

### Create

```python
def create(self, title: str, description: str = "") -> Task:
    """
    Create a new task and store it.
    
    Args:
        title: Task title (required, 1-200 chars)
        description: Task description (optional, max 1000 chars)
    
    Returns:
        The newly created Task object
    
    Raises:
        InvalidTaskDataError: If validation fails
    """
    # Validation happens in service layer
    task_id = self._generate_id()
    now = datetime.utcnow()
    
    task = Task(
        id=task_id,
        title=title.strip(),
        description=description.strip(),
        completed=False,
        created_at=now,
        updated_at=now
    )
    
    self._tasks[task_id] = task
    return task
```

### Read (Single)

```python
def get(self, task_id: int) -> Optional[Task]:
    """
    Retrieve a task by ID.
    
    Args:
        task_id: The task ID to retrieve
    
    Returns:
        Task object if found, None otherwise
    """
    return self._tasks.get(task_id)
```

### Read (All)

```python
def get_all(self) -> list[Task]:
    """
    Retrieve all tasks.
    
    Returns:
        List of all Task objects (may be empty)
    """
    return list(self._tasks.values())
```

### Update

```python
def update(self, task_id: int, title: str, description: str) -> Task:
    """
    Update an existing task.
    
    Args:
        task_id: The task ID to update
        title: New title (required, 1-200 chars)
        description: New description (optional, max 1000 chars)
    
    Returns:
        The updated Task object
    
    Raises:
        TaskNotFoundError: If task doesn't exist
    """
    task = self._tasks.get(task_id)
    if task is None:
        raise TaskNotFoundError(f"Task {task_id} not found")
    
    # Create updated task (dataclass is immutable pattern)
    updated_task = Task(
        id=task.id,
        title=title.strip(),
        description=description.strip(),
        completed=task.completed,
        created_at=task.created_at,
        updated_at=datetime.utcnow()
    )
    
    self._tasks[task_id] = updated_task
    return updated_task
```

### Delete

```python
def delete(self, task_id: int) -> bool:
    """
    Delete a task by ID.
    
    Args:
        task_id: The task ID to delete
    
    Returns:
        True if deleted, False if not found
    """
    if task_id in self._tasks:
        del self._tasks[task_id]
        return True
    return False
```

### Toggle Completion

```python
def toggle_completion(self, task_id: int) -> Task:
    """
    Toggle task completion status.
    
    Args:
        task_id: The task ID to toggle
    
    Returns:
        The updated Task object
    
    Raises:
        TaskNotFoundError: If task doesn't exist
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
```

---

## Validation Rules

### Title Validation

```python
def validate_title(title: str) -> None:
    """
    Validate task title.
    
    Raises:
        InvalidTaskDataError: If validation fails
    """
    if not title or len(title.strip()) == 0:
        raise InvalidTaskDataError("Title cannot be empty")
    
    if len(title) > 200:
        raise InvalidTaskDataError("Title cannot exceed 200 characters")
```

### Description Validation

```python
def validate_description(description: str) -> None:
    """
    Validate task description.
    
    Raises:
        InvalidTaskDataError: If validation fails
    """
    if len(description) > 1000:
        raise InvalidTaskDataError("Description cannot exceed 1000 characters")
```

---

## Error Handling

### Custom Exceptions

```python
class TaskNotFoundError(Exception):
    """Raised when a task ID doesn't exist in storage."""
    pass

class InvalidTaskDataError(Exception):
    """Raised when task data fails validation."""
    pass
```

### Error Scenarios

| Scenario | Exception | Message |
|----------|-----------|---------|
| Empty title | `InvalidTaskDataError` | "Title cannot be empty" |
| Title too long | `InvalidTaskDataError` | "Title cannot exceed 200 characters" |
| Description too long | `InvalidTaskDataError` | "Description cannot exceed 1000 characters" |
| Task not found (get) | Returns `None` | N/A |
| Task not found (update) | `TaskNotFoundError` | "Task {id} not found" |
| Task not found (toggle) | `TaskNotFoundError` | "Task {id} not found" |
| Task not found (delete) | Returns `False` | N/A |

---

## Data Lifecycle

### Task Creation Flow

```
User Input → Validation → ID Generation → Task Creation → Storage → Return Task
```

### Task Update Flow

```
User Input → Validation → Existence Check → Update Timestamp → Storage → Return Task
```

### Task Deletion Flow

```
User Input → Existence Check → Remove from Storage → Return Success/Failure
```

---

## Example Data

### Sample Tasks

```python
# Task 1: Pending
Task(
    id=1,
    title="Buy groceries",
    description="Milk, eggs, bread, butter",
    completed=False,
    created_at=datetime(2025, 12, 5, 10, 30, 0),
    updated_at=datetime(2025, 12, 5, 10, 30, 0)
)

# Task 2: Completed
Task(
    id=2,
    title="Call mom",
    description="",
    completed=True,
    created_at=datetime(2025, 12, 5, 9, 15, 0),
    updated_at=datetime(2025, 12, 5, 14, 20, 0)
)

# Task 3: Updated
Task(
    id=3,
    title="Finish project report",
    description="Include charts and summary",
    completed=False,
    created_at=datetime(2025, 12, 4, 16, 0, 0),
    updated_at=datetime(2025, 12, 5, 11, 45, 0)
)
```

---

## Future Considerations

### Phase II Migration (Database)

When migrating to PostgreSQL in Phase II:

- **ID Generation**: Use database auto-increment or sequences
- **Timestamps**: Use database timestamp functions
- **Validation**: Keep in service layer (database-agnostic)
- **Storage Interface**: Keep same method signatures for easy swap

### Potential Schema (PostgreSQL)

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Compliance Checklist

- ✅ Task model uses `@dataclass`
- ✅ All fields have type hints
- ✅ Validation rules defined
- ✅ ID generation strategy specified
- ✅ CRUD operations documented
- ✅ Error handling specified
- ✅ In-memory storage design clear
- ✅ Future migration path considered
