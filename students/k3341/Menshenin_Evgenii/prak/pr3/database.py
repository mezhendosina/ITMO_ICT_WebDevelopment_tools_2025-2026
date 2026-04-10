import os
from pathlib import Path

from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine

load_dotenv(Path(__file__).resolve().parent / ".env")

from models import Profession, Skill, SkillWarriorLink, Warrior  # noqa: F401, E402

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./warriors_prak.db")

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
