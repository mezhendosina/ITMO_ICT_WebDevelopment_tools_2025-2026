from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.database import get_session
from app.api.auth import get_current_user
from app.models.task import Task, TaskCreate, TaskUpdate, TaskRead
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=list[TaskRead])
def read_tasks(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    task_service = TaskService(session)
    return task_service.get_all(skip=skip, limit=limit)


@router.get("/hackathon/{hackathon_id}", response_model=list[TaskRead])
def read_tasks_by_hackathon(hackathon_id: int, session: Session = Depends(get_session)):
    task_service = TaskService(session)
    return task_service.get_by_hackathon(hackathon_id)


@router.get("/{task_id}", response_model=TaskRead)
def read_task(task_id: int, session: Session = Depends(get_session)):
    task_service = TaskService(session)
    task = task_service.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_create: TaskCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    task_service = TaskService(session)
    return task_service.create(task_create)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    task_service = TaskService(session)
    updated_task = task_service.update(task_id, task_update)

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    task_service = TaskService(session)
    success = task_service.delete(task_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
