# Constitution - Todo Console App

## Purpose

This constitution defines the foundational principles, coding standards, and architectural constraints for the Todo Console Application (Phase I of Hackathon II). All AI agents and developers must adhere to these guidelines.

---

## Core Principles

### 1. Spec-Driven Development
- **No code without specification**: Every feature must have a corresponding specification in `/specs` before implementation
- **Specification is the source of truth**: All implementation decisions must trace back to specs
- **Iterative refinement**: Specs can be updated, but changes must be documented

### 2. Simplicity First
- **YAGNI (You Aren't Gonna Need It)**: Implement only what's specified, no extra features
- **Clear over clever**: Prefer readable code over complex optimizations
- **Minimal dependencies**: Use Python standard library when possible

### 3. Separation of Concerns
- **Layered architecture**: Models → Storage → Services → UI
- **Single Responsibility**: Each module has one clear purpose
- **Loose coupling**: Layers communicate through well-defined interfaces

---

## Python Coding Standards

### Code Style
- **PEP 8 compliance**: Follow Python's official style guide
- **Type hints**: All function signatures must include type annotations
- **Docstrings**: All public functions and classes must have docstrings (Google style)
- **Line length**: Maximum 100 characters per line

### Naming Conventions
- **Classes**: `PascalCase` (e.g., `TaskService`, `MemoryStore`)
- **Functions/Methods**: `snake_case` (e.g., `add_task`, `get_all_tasks`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_TITLE_LENGTH`)
- **Private members**: Prefix with underscore (e.g., `_storage`)

### Type Hints
```python
# Required for all functions
def add_task(title: str, description: str) -> Task:
    """Add a new task to storage."""
    pass

# Use Optional for nullable values
from typing import Optional
def get_task(task_id: int) -> Optional[Task]:
    """Retrieve task by ID, returns None if not found."""
    pass
```

---

## Architecture Principles

### Project Structure
```
d:\Hackathon\
├── constitution.md          # This file
├── specs/                   # Specifications
│   ├── overview.md
│   ├── features/
│   │   └── task-crud.md
│   └── data-model.md
├── src/                     # Source code
│   ├── models/              # Data models
│   │   └── task.py
│   ├── storage/             # Storage layer
│   │   └── memory_store.py
│   ├── services/            # Business logic
│   │   └── task_service.py
│   ├── ui/                  # User interface
│   │   └── console_ui.py
│   └── main.py              # Entry point
├── README.md                # User documentation
├── CLAUDE.md                # AI agent instructions
├── AGENTS.md                # Agent behavior guide
└── pyproject.toml           # UV configuration
```

### Layer Responsibilities

#### Models (`src/models/`)
- **Purpose**: Define data structures
- **Rules**: 
  - Use `@dataclass` for simplicity
  - Immutable where possible
  - No business logic
  - Type hints required

#### Storage (`src/storage/`)
- **Purpose**: Manage data persistence (in-memory for Phase I)
- **Rules**:
  - CRUD operations only
  - No business logic
  - Return data models
  - Handle ID generation

#### Services (`src/services/`)
- **Purpose**: Implement business logic
- **Rules**:
  - Validate inputs
  - Enforce business rules
  - Coordinate between storage and UI
  - Handle errors gracefully

#### UI (`src/ui/`)
- **Purpose**: User interaction
- **Rules**:
  - Display formatting only
  - Input collection and validation
  - No business logic
  - Clear error messages

---

## Data Model Standards

### Task Model
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    """Represents a single todo task."""
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime
```

### Validation Rules
- **Title**: Required, 1-200 characters, non-empty after strip
- **Description**: Optional, max 1000 characters
- **ID**: Auto-generated, positive integer, unique
- **Timestamps**: Auto-managed, UTC timezone

---

## Error Handling

### Principles
- **Fail fast**: Validate inputs early
- **Clear messages**: User-friendly error descriptions
- **No silent failures**: Always communicate errors
- **Graceful degradation**: Don't crash on invalid input

### Error Types
```python
# Custom exceptions for clarity
class TaskNotFoundError(Exception):
    """Raised when task ID doesn't exist."""
    pass

class InvalidTaskDataError(Exception):
    """Raised when task data fails validation."""
    pass
```

### Error Handling Pattern
```python
def update_task(task_id: int, title: str, description: str) -> Task:
    """Update task with validation."""
    # Validate inputs
    if not title or len(title.strip()) == 0:
        raise InvalidTaskDataError("Title cannot be empty")
    
    # Check existence
    task = storage.get(task_id)
    if task is None:
        raise TaskNotFoundError(f"Task {task_id} not found")
    
    # Perform operation
    return storage.update(task_id, title, description)
```

---

## In-Memory Storage Design

### Storage Structure
```python
# Dictionary-based storage
_tasks: dict[int, Task] = {}
_next_id: int = 1
```

### Concurrency
- **Phase I**: Single-threaded, no locking needed
- **Future phases**: Consider thread safety

### Data Lifecycle
- **Session-based**: Data exists only while app runs
- **No persistence**: Data lost on exit (expected behavior)
- **Clean state**: Each run starts fresh

---

## Testing Approach

### Phase I: Manual Testing
- **Interactive verification**: Test each feature through console
- **Edge cases**: Empty inputs, invalid IDs, special characters
- **User scenarios**: Complete workflows (add → view → update → complete → delete)

### Test Checklist
- ✅ Add task with valid data
- ✅ Add task with empty title (should fail)
- ✅ View empty task list
- ✅ View populated task list
- ✅ Update existing task
- ✅ Update non-existent task (should fail)
- ✅ Delete existing task
- ✅ Delete non-existent task (should fail)
- ✅ Mark task complete/incomplete
- ✅ Toggle completion multiple times

---

## Performance Standards

### Phase I Requirements
- **Response time**: Instant (< 100ms for any operation)
- **Memory**: Minimal (< 10MB for reasonable task count)
- **Startup**: < 1 second

### Scalability Considerations
- **Current**: Support 1000+ tasks in memory
- **Future**: Design allows migration to database

---

## Security & Privacy

### Phase I Scope
- **No authentication**: Single-user console app
- **No network**: Offline only
- **No sensitive data**: Plain text storage acceptable

### Input Sanitization
- **Prevent injection**: No eval() or exec()
- **Validate types**: Use type hints and runtime checks
- **Limit lengths**: Enforce max string lengths

---

## Documentation Standards

### Code Documentation
```python
def add_task(title: str, description: str = "") -> Task:
    """
    Create a new task and add it to storage.
    
    Args:
        title: Task title (required, 1-200 chars)
        description: Task description (optional, max 1000 chars)
    
    Returns:
        The newly created Task object
    
    Raises:
        InvalidTaskDataError: If title is empty or too long
    """
    pass
```

### User Documentation
- **README.md**: Setup, installation, usage
- **CLAUDE.md**: AI agent instructions
- **Inline help**: Console menu with clear options

---

## Version Control

### Git Practices
- **Meaningful commits**: Descriptive commit messages
- **Atomic commits**: One logical change per commit
- **Branch strategy**: Main branch for stable code

### .gitignore
```
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
.idea/
.vscode/
*.swp
*.swo
```

---

## Agent Behavior Rules

### Code Generation
- **Spec compliance**: Generated code must match specifications exactly
- **No improvisation**: Don't add features not in specs
- **Ask when unclear**: Request clarification rather than assume

### Modification Rules
- **Update specs first**: Changes to requirements require spec updates
- **Maintain consistency**: Follow existing patterns
- **Document changes**: Update relevant documentation

### Reference Format
```python
# [Spec]: specs/features/task-crud.md § Add Task
# [Task]: T-001
def add_task(title: str, description: str = "") -> Task:
    """Implementation per specification."""
    pass
```

---

## Future-Proofing

### Design for Evolution
- **Database migration**: Storage layer abstraction allows easy swap
- **API addition**: Services layer can be exposed via REST API
- **Multi-user**: Architecture supports adding authentication
- **Persistence**: In-memory store can be replaced with file/DB

### What NOT to Implement Now
- ❌ Database integration
- ❌ User authentication
- ❌ Network features
- ❌ GUI
- ❌ Advanced features (priorities, tags, due dates)

---

## Compliance Checklist

Before considering any code complete, verify:

- ✅ Specification exists and is followed
- ✅ Type hints on all functions
- ✅ Docstrings on all public APIs
- ✅ PEP 8 compliant
- ✅ Error handling implemented
- ✅ Layer separation maintained
- ✅ Manual testing completed
- ✅ Documentation updated

---

## Amendment Process

This constitution can be updated when:
1. New requirements emerge
2. Better patterns are discovered
3. Phase progression requires changes

**Process**: Update constitution → Update affected specs → Regenerate code
