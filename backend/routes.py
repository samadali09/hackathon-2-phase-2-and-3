from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime
from models import Task, TaskCreate, TaskUpdate
from database import get_session
from auth import get_current_user_id, verify_user_access

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])

@router.get("", response_model=List[Task])
async def list_tasks(user_id: str, current_user_id: str = Depends(get_current_user_id), session: Session = Depends(get_session)):
    verify_user_access(user_id, current_user_id)
    # Query using 'completed' logic
    statement = select(Task).where(Task.user_id == user_id)
    return session.exec(statement).all()

@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(user_id: str, task_data: TaskCreate, current_user_id: str = Depends(get_current_user_id), session: Session = Depends(get_session)):
    verify_user_access(user_id, current_user_id)
    # Task model uses a string 'status' field, not 'completed' boolean
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        status="pending",
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Delete a task by ID for the given user.
    """
    verify_user_access(user_id, current_user_id)
    task = session.get(Task, task_id)
    if not task or str(task.user_id) != str(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    session.delete(task)
    session.commit()
    # 204: no body needed