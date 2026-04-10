from typing import List, Optional
from sqlmodel import Session, select
from app.models.task import Task, TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Task]:
        statement = select(Task).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.session.get(Task, task_id)

    def get_by_hackathon(self, hackathon_id: int) -> List[Task]:
        statement = select(Task).where(Task.hackathon_id == hackathon_id)
        return list(self.session.exec(statement).all())

    def create(self, task_create: TaskCreate) -> Task:
        task = Task(**task_create.model_dump())
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def update(self, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        task = self.get_by_id(task_id)
        if not task:
            return None

        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task_id: int) -> bool:
        task = self.get_by_id(task_id)
        if not task:
            return False

        self.session.delete(task)
        self.session.commit()
        return True
