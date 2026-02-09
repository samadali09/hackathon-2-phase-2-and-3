from typing import Optional
from sqlmodel import Session, select
from database import engine
from models import Task
from datetime import datetime
from datetime import datetime

class MCPTools:
    def add_task(self, user_id: str, title: str, description: Optional[str] = None):
        with Session(engine) as session:
            task = Task(user_id=user_id, title=title, description=description)
            session.add(task)
            session.commit()
            session.refresh(task)
            return {"id": task.id, "title": task.title, "status": "created"}

    def list_tasks(self, user_id: str, status: Optional[str] = None):
        with Session(engine) as session:
            statement = select(Task).where(Task.user_id == user_id)
            if status:
                statement = statement.where(Task.status == status)
            tasks = session.exec(statement).all()
            return [{"id": t.id, "title": t.title, "description": t.description, "status": t.status} for t in tasks]

    def complete_task(self, user_id: str, task_id: int):
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if not task or task.user_id != user_id:
                return {"error": "Task not found or unauthorized"}
            task.status = "completed"
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)
            return {"id": task.id, "title": task.title, "status": task.status}

    def delete_task(self, user_id: str, task_id: int):
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if not task or task.user_id != user_id:
                return {"error": "Task not found or unauthorized"}
            session.delete(task)
            session.commit()
            return {"status": "success", "message": f"Task {task_id} deleted."}

    def update_task(self, user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None, status: Optional[str] = None):
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if not task or task.user_id != user_id:
                return {"error": "Task not found or unauthorized"}
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if status is not None:
                task.status = status
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)
            return {"id": task.id, "title": task.title, "description": task.description, "status": task.status}

def get_gemini_tool_definitions():
    return [{"function_declarations": [
        {"name": "add_task", "description": "Add a new task to the user's todo list.",
         "parameters": {"type": "object", "properties": {"title": {"type": "string", "description": "The title of the task"}, "description": {"type": "string", "description": "A detailed description of the task"}}, "required": ["title"]}},
        {"name": "list_tasks", "description": "List all tasks for the current user, optionally filtered by status.",
         "parameters": {"type": "object", "properties": {"status": {"type": "string", "description": "Filter tasks by status. Can be 'pending' or 'completed'. If not provided, all tasks are returned."}}, "required": []}},
        {"name": "complete_task", "description": "Mark a specific task as completed.",
         "parameters": {"type": "object", "properties": {"task_id": {"type": "integer", "description": "The ID of the task to mark as complete."}}, "required": ["task_id"]}},
        {"name": "delete_task", "description": "Delete a task from the user's todo list.",
         "parameters": {"type": "object", "properties": {"task_id": {"type": "integer", "description": "The ID of the task to delete."}}, "required": ["task_id"]}},
        {"name": "update_task", "description": "Update the title, description, or status of an existing task.",
         "parameters": {"type": "object", "properties": {"task_id": {"type": "integer", "description": "The ID of the task to update."}, "title": {"type": "string", "description": "The new title for the task (optional)."}, "description": {"type": "string", "description": "The new description for the task (optional)."}, "status": {"type": "string", "description": "The new status for the task (e.g., 'pending' or 'completed') (optional)."}}, "required": ["task_id"]}}
    ]}]