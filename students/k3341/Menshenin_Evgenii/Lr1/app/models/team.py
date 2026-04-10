from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .participant import Participant
    from .submission import Submission


class TeamBase(SQLModel):
    name: str
    description: Optional[str] = None


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hackathon_id: int = Field(foreign_key="hackathon.id")
    creator_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    creator: "User" = Relationship(back_populates="teams_created")
    members: list["Participant"] = Relationship(back_populates="team")
    hackathon: "Hackathon" = Relationship(back_populates="teams")
    submissions: list["Submission"] = Relationship(back_populates="team")


class TeamCreate(TeamBase):
    hackathon_id: int


class TeamUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TeamRead(TeamBase):
    id: int
    hackathon_id: int
    creator_id: int
    created_at: datetime
