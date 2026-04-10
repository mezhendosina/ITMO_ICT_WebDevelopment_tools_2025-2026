from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .hackathon import Hackathon
    from .team import Team


class ParticipantBase(SQLModel):
    role: str = Field(description="Role of the participant in the hackathon")


class Participant(ParticipantBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    hackathon_id: int = Field(foreign_key="hackathon.id")
    registered_at: datetime = Field(default_factory=datetime.utcnow)
    team_id: Optional[int] = Field(foreign_key="team.id", default=None)

    user: "User" = Relationship(back_populates="participations")
    hackathon: "Hackathon" = Relationship(back_populates="participants")
    team: Optional["Team"] = Relationship(back_populates="members")


class ParticipantCreate(ParticipantBase):
    user_id: int
    hackathon_id: int


class ParticipantRead(ParticipantBase):
    id: int
    user_id: int
    hackathon_id: int
    registered_at: datetime
    team_id: Optional[int] = None


class ParticipantUpdate(SQLModel):
    role: Optional[str] = None
    team_id: Optional[int] = None


class ParticipantWithHackathon(ParticipantRead):
    hackathon_title: Optional[str] = None
    user_name: Optional[str] = None


from .team import Team
