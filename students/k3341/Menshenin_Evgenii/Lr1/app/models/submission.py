from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .team import Team
    from .task import Task
    from .evaluation import Evaluation


class SubmissionBase(SQLModel):
    description: str
    project_link: Optional[str] = None


class Submission(SubmissionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    task_id: int = Field(foreign_key="task.id")
    team_id: Optional[int] = Field(foreign_key="team.id")
    submitted_at: datetime = Field(default_factory=datetime.utcnow)

    user: "User" = Relationship(back_populates="submissions")
    task: "Task" = Relationship(back_populates="submissions")
    team: Optional["Team"] = Relationship(back_populates="submissions")
    evaluations: list["Evaluation"] = Relationship(back_populates="submission")


class SubmissionCreate(SubmissionBase):
    task_id: int
    team_id: Optional[int] = None


class SubmissionUpdate(SQLModel):
    description: Optional[str] = None
    project_link: Optional[str] = None


class SubmissionRead(SubmissionBase):
    id: int
    user_id: int
    task_id: int
    team_id: Optional[int]
    submitted_at: datetime
