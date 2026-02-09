# Claude Code Instructions

## Project Context

This is **Phase I of Hackathon II**: Todo In-Memory Python Console App.

**Critical Constraint**: All code must be generated through spec-driven development. No manual coding allowed.

---

## How to Navigate This Project

### 1. Start with the Constitution
Read [@constitution.md](file:///d:/Hackathon/constitution.md) to understand:
- Coding standards (PEP 8, type hints, docstrings)
- Architecture principles (layered design, separation of concerns)
- Error handling patterns
- Project structure

### 2. Review Specifications
All requirements are in the `/specs` folder:
- [@specs/overview.md](file:///d:/Hackathon/specs/overview.md) - Project overview
- [@specs/data-model.md](file:///d:/Hackathon/specs/data-model.md) - Task model and storage
- [@specs/features/task-crud.md](file:///d:/Hackathon/specs/features/task-crud.md) - All 5 features

### 3. Understand Agent Behavior
Read [@AGENTS.md](file:///d:/Hackathon/AGENTS.md) for:
- Spec-driven workflow (Specify → Plan → Tasks → Implement)
- Agent behavior rules
- Reference patterns

---

## Implementation Guidelines

### Code Generation Rules

1. **Always reference specifications**:
```python
# [Spec]: specs/features/task-crud.md § Add Task
# [Constitution]: constitution.md § Validation Rules
def add_task(title: str, description: str = "") -> Task:
    """Create a new task per specification."""
    pass
```

2. **Follow the layered architecture**:
   - `src/models/` - Data structures only
   - `src/storage/` - CRUD operations only
   - `src/services/` - Business logic and validation
   - `src/ui/` - User interaction only
   - `src/main.py` - Application entry point

3. **Use type hints everywhere**:
```python
def get_task(task_id: int) -> Optional[Task]:
    """Retrieve task by ID."""
    pass
```

4. **Write docstrings (Google style)**:
```python
def update_task(task_id: int, title: str, description: str) -> Task:
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
        InvalidTaskDataError: If validation fails
    """
    pass
```

5. **Implement error handling**:
```python
class TaskNotFoundError(Exception):
    """Raised when task ID doesn't exist."""
    pass

class InvalidTaskDataError(Exception):
    """Raised when task data fails validation."""
    pass
```

---

## Project Structure

```
d:\Hackathon\
├── constitution.md          # Principles and standards
├── specs/                   # Specifications
│   ├── overview.md
│   ├── features/
│   │   └── task-crud.md
│   └── data-model.md
├── src/                     # Source code
│   ├── models/
│   │   └── task.py         # Task dataclass
│   ├── storage/
│   │   └── memory_store.py # In-memory storage
│   ├── services/
│   │   └── task_service.py # Business logic
│   ├── ui/
│   │   └── console_ui.py   # Console interface
│   └── main.py             # Entry point
├── README.md               # User documentation
├── CLAUDE.md               # This file
├── AGENTS.md               # Agent behavior guide
└── pyproject.toml          # UV configuration
```

---

## Development Workflow

### When implementing a feature:

1. **Read the specification**:
   - [@specs/features/task-crud.md](file:///d:/Hackathon/specs/features/task-crud.md) for feature details
   - [@specs/data-model.md](file:///d:/Hackathon/specs/data-model.md) for data structures

2. **Check the constitution**:
   - [@constitution.md](file:///d:/Hackathon/constitution.md) for coding standards

3. **Generate code layer by layer**:
   - Start with models (`src/models/task.py`)
   - Then storage (`src/storage/memory_store.py`)
   - Then services (`src/services/task_service.py`)
   - Then UI (`src/ui/console_ui.py`)
   - Finally main (`src/main.py`)

4. **Follow acceptance criteria**:
   - Each feature has detailed acceptance criteria in specs
   - Implement exactly what's specified
   - Don't add extra features

---

## Tech Stack

- **Python**: 3.13+
- **Package Manager**: UV
- **Dependencies**: Standard library only (no external packages)
- **Data Structures**: `@dataclass` for models, `dict` for storage

---

## Running the Application

```bash
# Using UV
uv run python src/main.py

# Or with standard Python
python src/main.py
```

---

## Testing Approach

Phase I uses **manual testing**:

1. Run the application
2. Test each feature:
   - Add Task (valid and invalid inputs)
   - View Tasks (empty and populated)
   - Update Task (existing and non-existent)
   - Delete Task (with confirmation)
   - Mark Complete (toggle multiple times)
3. Verify against acceptance criteria in specs

---

## Key Principles

### 1. Spec-Driven Development
- ✅ Code must match specifications exactly
- ✅ No improvisation or "creative" solutions
- ✅ Ask for clarification if specs are unclear

### 2. Clean Architecture
- ✅ Strict layer separation
- ✅ Single responsibility per module
- ✅ No business logic in UI or storage layers

### 3. Type Safety
- ✅ Type hints on all functions
- ✅ Use `Optional` for nullable values
- ✅ Use `dataclass` for data models

### 4. Error Handling
- ✅ Validate inputs early
- ✅ Clear error messages
- ✅ No silent failures
- ✅ Graceful degradation

---

## What NOT to Implement

Phase I scope is limited. Do NOT implement:
- ❌ Database persistence
- ❌ File storage
- ❌ User authentication
- ❌ Network features
- ❌ GUI
- ❌ Advanced features (priorities, tags, due dates, search, filter)

---

## Reference Patterns

### When implementing a feature:
```
Read: @specs/features/task-crud.md § [Feature Name]
Follow: @constitution.md § [Relevant Section]
Implement: src/[layer]/[file].py
```

### When unsure:
```
1. Check specification first
2. Check constitution second
3. Ask for clarification if still unclear
```

---

## Success Criteria

Code is complete when:
- ✅ All 5 Basic Level features work
- ✅ Follows all constitution principles
- ✅ Matches specifications exactly
- ✅ Passes manual testing
- ✅ Has complete documentation
- ✅ Ready for GitHub submission

---

## Quick Links

- [Constitution](file:///d:/Hackathon/constitution.md) - Principles and standards
- [Overview](file:///d:/Hackathon/specs/overview.md) - Project overview
- [Data Model](file:///d:/Hackathon/specs/data-model.md) - Task structure
- [Features](file:///d:/Hackathon/specs/features/task-crud.md) - All 5 features
- [Agent Guide](file:///d:/Hackathon/AGENTS.md) - Agent behavior

---

## Remember

**No manual coding allowed!** All code must be generated through Claude Code based on these specifications. Refine specs if needed, but never write code directly.
