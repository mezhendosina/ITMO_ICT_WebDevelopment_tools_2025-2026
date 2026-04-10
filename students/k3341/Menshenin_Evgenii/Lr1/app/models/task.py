from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .hackathon import Hackathon
    from .submission import Submission
    from .task import Task


class TaskBase(SQLModel):
    title: str
    description: str
    requirements: str
    criteria: str
    max_score: int = Field(default=100)


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hackathon_id: int = Field(foreign_key="hackathon.id")

    hackathon: "Hackathon" = Relationship(back_populates="tasks")
    submissions: list["Submission"] = Relationship(back_populates="task")


class TaskCreate(TaskBase):
    hackathon_id: int


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    criteria: Optional[str] = None
    max_score: Optional[int] = None


class TaskRead(TaskBase):
    id: int
    hackathon_id: int
