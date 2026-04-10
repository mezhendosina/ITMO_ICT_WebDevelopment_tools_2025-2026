from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .hackathon import Hackathon, Participant
    from .team import Team
    from .submission import Submission
    from .evaluation import Evaluation


class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)
    full_name: str
    phone: Optional[str] = None
    skills: Optional[str] = None


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

    hackathons: list["Hackathon"] = Relationship(back_populates="organizer")
    participations: list["Participant"] = Relationship(back_populates="user")
    teams_created: list["Team"] = Relationship(back_populates="creator")
    submissions: list["Submission"] = Relationship(back_populates="user")
    evaluations_given: list["Evaluation"] = Relationship(back_populates="evaluator")


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    skills: Optional[str] = None
    password: Optional[str] = None


class UserRead(UserBase):
    id: int


class UserLogin(SQLModel):
    email: str
    password: str
