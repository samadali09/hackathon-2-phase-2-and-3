# Todo App - Project Overview

## Purpose

A todo application that evolves from a simple console app to a cloud-native AI-powered chatbot. This document describes Phase I: the foundational in-memory Python console application.

---

## Current Phase

**Phase I: Todo In-Memory Python Console App**

**Status**: In Development  
**Due Date**: December 7, 2025  
**Points**: 100

---

## Project Vision

This project demonstrates the evolution of software from simple scripts to distributed cloud-native systems:

- **Phase I**: Console app (in-memory storage)
- **Phase II**: Full-stack web app (Next.js + FastAPI + PostgreSQL)
- **Phase III**: AI chatbot (OpenAI Agents SDK + MCP)
- **Phase IV**: Local Kubernetes (Minikube + Helm)
- **Phase V**: Cloud deployment (DigitalOcean + Kafka + Dapr)

---

## Phase I Objectives

### Primary Goal
Build a command-line todo application using **spec-driven development** with Claude Code and Spec-Kit Plus.

### Key Constraints
- ✅ **Spec-driven**: All code generated from specifications
- ✅ **No manual coding**: Refine specs until Claude Code generates correct output
- ✅ **In-memory storage**: No database or file persistence
- ✅ **Clean architecture**: Proper separation of concerns

---

## Tech Stack

### Core Technologies
- **Language**: Python 3.13+
- **Package Manager**: UV
- **Development Approach**: Spec-Driven Development
- **AI Tools**: Claude Code, Spec-Kit Plus

### Dependencies
- **Standard Library Only**: No external packages for Phase I
- **Type Hints**: Full type annotation support
- **Dataclasses**: For data models

---

## Features

### Basic Level (Phase I Scope)

#### ✅ Add Task
Create new todo items with title and description.

**User Story**: As a user, I can add a task so that I can track things I need to do.

#### ✅ View Task List
Display all tasks with their details and status.

**User Story**: As a user, I can view all my tasks so that I know what needs to be done.

#### ✅ Update Task
Modify existing task details (title and description).

**User Story**: As a user, I can update a task so that I can correct or clarify information.

#### ✅ Delete Task
Remove tasks from the list.

**User Story**: As a user, I can delete a task so that I can remove completed or cancelled items.

#### ✅ Mark as Complete
Toggle task completion status.

**User Story**: As a user, I can mark a task as complete so that I can track my progress.

### Out of Scope for Phase I
- ❌ Priorities & Tags
- ❌ Search & Filter
- ❌ Due Dates & Reminders
- ❌ Recurring Tasks
- ❌ Persistence (file/database)
- ❌ Multi-user support
- ❌ Authentication

---

## Architecture

### Layered Design

```
┌─────────────────────────────────────┐
│         Console UI Layer            │
│    (User interaction & display)     │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│        Service Layer                │
│   (Business logic & validation)     │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│        Storage Layer                │
│     (In-memory data management)     │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│         Model Layer                 │
│      (Data structures)              │
└─────────────────────────────────────┘
```

### Component Responsibilities

| Layer | Responsibility | Files |
|-------|---------------|-------|
| **Models** | Define data structures | `src/models/task.py` |
| **Storage** | Manage in-memory data | `src/storage/memory_store.py` |
| **Services** | Business logic & validation | `src/services/task_service.py` |
| **UI** | User interaction | `src/ui/console_ui.py` |
| **Main** | Application entry point | `src/main.py` |

---

## Data Model

### Task Entity

```python
@dataclass
class Task:
    id: int                    # Auto-generated unique identifier
    title: str                 # Task title (required, 1-200 chars)
    description: str           # Task description (optional, max 1000 chars)
    completed: bool            # Completion status (default: False)
    created_at: datetime       # Creation timestamp (auto-set)
    updated_at: datetime       # Last update timestamp (auto-managed)
```

---

## User Interface

### Console Menu

```
=== Todo App ===
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Enter your choice:
```

### Task Display Format

```
ID: 1
Title: Buy groceries
Description: Milk, eggs, bread
Status: Pending
Created: 2025-12-01 10:30:00
Updated: 2025-12-01 10:30:00
---
```

---

## Development Workflow

### Spec-Driven Process

1. **Specify**: Write detailed specifications in `/specs`
2. **Plan**: Create implementation plan
3. **Tasks**: Break down into atomic tasks
4. **Implement**: Claude Code generates code from specs
5. **Verify**: Manual testing against acceptance criteria
6. **Iterate**: Refine specs if needed, regenerate code

### No Manual Coding Rule

❌ **Not Allowed**: Writing code directly  
✅ **Required**: Refine specifications until Claude Code generates correct implementation

---

## Quality Standards

### Code Quality
- ✅ PEP 8 compliant
- ✅ Type hints on all functions
- ✅ Docstrings on all public APIs
- ✅ Proper error handling
- ✅ Clean separation of concerns

### Testing
- ✅ Manual testing of all features
- ✅ Edge case validation
- ✅ User scenario walkthroughs

### Documentation
- ✅ README.md with setup instructions
- ✅ CLAUDE.md with AI agent guidelines
- ✅ Inline code documentation
- ✅ Specification files

---

## Success Criteria

Phase I is complete when:

- ✅ All 5 Basic Level features work correctly
- ✅ Application runs without errors
- ✅ Tasks persist in memory during session
- ✅ User-friendly console interface
- ✅ Clean, well-structured code
- ✅ Complete documentation
- ✅ All specs followed precisely
- ✅ Ready for GitHub submission

---

## Deliverables

### GitHub Repository Structure

```
d:\Hackathon\
├── constitution.md
├── specs/
│   ├── overview.md (this file)
│   ├── features/
│   │   └── task-crud.md
│   └── data-model.md
├── src/
│   ├── models/
│   ├── storage/
│   ├── services/
│   ├── ui/
│   └── main.py
├── README.md
├── CLAUDE.md
├── AGENTS.md
├── pyproject.toml
└── .gitignore
```

### Submission Requirements
- ✅ Public GitHub repository
- ✅ Working console application
- ✅ Complete documentation
- ✅ Demo video (< 90 seconds)

---

## Timeline

| Milestone | Date | Status |
|-----------|------|--------|
| Specifications Complete | Dec 5, 2025 | In Progress |
| Implementation Complete | Dec 6, 2025 | Pending |
| Testing & Documentation | Dec 6, 2025 | Pending |
| Submission | Dec 7, 2025 | Pending |

---

## Next Steps

1. Complete all specification files
2. Set up development environment (UV, Python 3.13+)
3. Generate implementation via Claude Code
4. Manual testing and verification
5. Prepare submission materials
6. Submit by December 7, 2025

---

## References

- **Hackathon Documentation**: Full requirements document
- **Constitution**: [constitution.md](file:///d:/Hackathon/constitution.md)
- **Feature Specs**: [specs/features/task-crud.md](file:///d:/Hackathon/specs/features/task-crud.md)
- **Data Model**: [specs/data-model.md](file:///d:/Hackathon/specs/data-model.md)
