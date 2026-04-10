from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .participant import Participant
    from .task import Task
    from .team import Team


class HackathonBase(SQLModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    max_participants: Optional[int] = None


class Hackathon(HackathonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    organizer_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    organizer: "User" = Relationship(back_populates="hackathons")
    participants: list["Participant"] = Relationship(back_populates="hackathon")
    tasks: list["Task"] = Relationship(back_populates="hackathon")
    teams: list["Team"] = Relationship(back_populates="hackathon")


class HackathonCreate(HackathonBase):
    pass


class HackathonUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    max_participants: Optional[int] = None


class HackathonRead(HackathonBase):
    id: int
    organizer_id: int
    created_at: datetime
