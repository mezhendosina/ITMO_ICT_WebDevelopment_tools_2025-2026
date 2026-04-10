from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class RaceType(str, Enum):
    director = "director"
    worker = "worker"
    junior = "junior"


class SkillWarriorLink(SQLModel, table=True):
    skill_id: Optional[int] = Field(
        default=None, foreign_key="skill.id", primary_key=True
    )
    warrior_id: Optional[int] = Field(
        default=None, foreign_key="warrior.id", primary_key=True
    )


class Skill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = ""
    warriors: List["Warrior"] = Relationship(
        back_populates="skills", link_model=SkillWarriorLink
    )


class Profession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    warriors_prof: List["Warrior"] = Relationship(back_populates="profession")


class Warrior(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    race: RaceType
    name: str
    level: int
    profession_id: Optional[int] = Field(default=None, foreign_key="profession.id")
    profession: Optional[Profession] = Relationship(back_populates="warriors_prof")
    skills: List["Skill"] = Relationship(
        back_populates="warriors", link_model=SkillWarriorLink
    )


class ProfessionRead(SQLModel):
    id: int
    title: str
    description: str

    model_config = {"from_attributes": True}


class ProfessionCreate(SQLModel):
    title: str
    description: str


class ProfessionUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None


class SkillRead(SQLModel):
    id: int
    name: str
    description: Optional[str] = ""

    model_config = {"from_attributes": True}


class SkillCreate(SQLModel):
    name: str
    description: Optional[str] = ""


class SkillUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None


class WarriorShort(SQLModel):
    id: int
    race: RaceType
    name: str
    level: int
    profession_id: Optional[int] = None

    model_config = {"from_attributes": True}


class WarriorRead(SQLModel):
    id: int
    race: RaceType
    name: str
    level: int
    profession_id: Optional[int] = None
    profession: ProfessionRead
    skills: List[SkillRead] = []

    model_config = {"from_attributes": True}


class WarriorCreate(SQLModel):
    race: RaceType
    name: str
    level: int
    profession_id: int


class WarriorUpdate(SQLModel):
    race: Optional[RaceType] = None
    name: Optional[str] = None
    level: Optional[int] = None
    profession_id: Optional[int] = None
