from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .submission import Submission


class EvaluationBase(SQLModel):
    score: int = Field(ge=0, le=100)
    comments: Optional[str] = None


class Evaluation(EvaluationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    submission_id: int = Field(foreign_key="submission.id")
    evaluator_id: int = Field(foreign_key="user.id")

    submission: "Submission" = Relationship(back_populates="evaluations")
    evaluator: "User" = Relationship(back_populates="evaluations_given")


class EvaluationCreate(EvaluationBase):
    submission_id: int


class EvaluationUpdate(SQLModel):
    score: Optional[int] = None
    comments: Optional[str] = None


class EvaluationRead(EvaluationBase):
    id: int
    submission_id: int
    evaluator_id: int
