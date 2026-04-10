from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class RaceType(str, Enum):
    director = "director"
    worker = "worker"
    junior = "junior"


class Profession(BaseModel):
    id: int
    title: str
    description: str


class Skill(BaseModel):
    id: int
    name: str
    description: str = ""


class Warrior(BaseModel):
    id: int
    race: RaceType
    name: str
    level: int
    profession: Profession
    skills: List[Skill] = Field(default_factory=list)
