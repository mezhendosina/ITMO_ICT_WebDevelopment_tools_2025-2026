from pathlib import Path
from typing import Annotated, Optional

from alembic import command
from alembic.config import Config
from fastapi import Body, Depends, FastAPI, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from database import engine, get_session
from models import (
    Profession,
    ProfessionCreate,
    ProfessionRead,
    ProfessionUpdate,
    RaceType,
    Skill,
    SkillCreate,
    SkillLinkBody,
    SkillRead,
    SkillUpdate,
    SkillWarriorLink,
    SkillWithLevelRead,
    Warrior,
    WarriorCreate,
    WarriorRead,
    WarriorShort,
    WarriorUpdate,
)

app = FastAPI(title="Практика 1.3 — воины (Alembic + level)")


def run_migrations() -> None:
    cfg = Config(str(Path(__file__).resolve().parent / "alembic.ini"))
    command.upgrade(cfg, "head")


@app.on_event("startup")
def on_startup() -> None:
    run_migrations()
    with Session(engine) as session:
        seed_if_empty(session)


def seed_if_empty(session: Session) -> None:
    if session.exec(select(Profession)).first():
        return
    p1 = Profession(title="Влиятельный человек", description="Эксперт по всем вопросам")
    p2 = Profession(title="Дельфист-гребец", description="Уважаемый сотрудник")
    session.add(p1)
    session.add(p2)
    session.commit()
    session.refresh(p1)
    session.refresh(p2)

    s1 = Skill(name="Купле-продажа компрессоров", description="")
    s2 = Skill(name="Оценка имущества", description="")
    session.add(s1)
    session.add(s2)
    session.commit()
    session.refresh(s1)
    session.refresh(s2)

    w1 = Warrior(
        race=RaceType.director,
        name="Мартынов Дмитрий",
        level=12,
        profession_id=p1.id,
    )
    w2 = Warrior(
        race=RaceType.worker,
        name="Андрей Косякин",
        level=12,
        profession_id=p2.id,
    )
    session.add(w1)
    session.add(w2)
    session.commit()
    session.refresh(w1)
    session.refresh(w2)

    session.add(SkillWarriorLink(skill_id=s1.id, warrior_id=w1.id, level=5))
    session.add(SkillWarriorLink(skill_id=s2.id, warrior_id=w1.id, level=3))
    session.commit()


def build_warrior_read(session: Session, w: Warrior) -> WarriorRead:
    session.refresh(w, attribute_names=["profession"])
    if w.profession is None:
        raise HTTPException(status_code=500, detail="Profession not loaded")

    stmt = (
        select(Skill, SkillWarriorLink)
        .join(SkillWarriorLink, SkillWarriorLink.skill_id == Skill.id)
        .where(SkillWarriorLink.warrior_id == w.id)
    )
    skill_rows = session.exec(stmt).all()
    skills = [
        SkillWithLevelRead(
            id=s.id,
            name=s.name,
            description=s.description or "",
            level=lnk.level,
        )
        for s, lnk in skill_rows
    ]

    return WarriorRead(
        id=w.id,
        race=w.race,
        name=w.name,
        level=w.level,
        profession_id=w.profession_id,
        profession=ProfessionRead.model_validate(w.profession),
        skills=skills,
    )


@app.get("/")
def hello() -> str:
    return "Hello, warrior (Alembic)!"


@app.get("/professions", response_model=list[ProfessionRead])
def list_professions(session: Session = Depends(get_session)) -> list[Profession]:
    return list(session.exec(select(Profession)).all())


@app.get("/profession/{profession_id}", response_model=ProfessionRead)
def get_profession(profession_id: int, session: Session = Depends(get_session)) -> Profession:
    p = session.get(Profession, profession_id)
    if not p:
        raise HTTPException(status_code=404, detail="Profession not found")
    return p


@app.post("/profession", response_model=ProfessionRead, status_code=201)
def create_profession(
    body: ProfessionCreate, session: Session = Depends(get_session)
) -> Profession:
    p = Profession(**body.model_dump())
    session.add(p)
    session.commit()
    session.refresh(p)
    return p


@app.put("/profession/{profession_id}", response_model=ProfessionRead)
def update_profession(
    profession_id: int,
    body: ProfessionUpdate,
    session: Session = Depends(get_session),
) -> Profession:
    p = session.get(Profession, profession_id)
    if not p:
        raise HTTPException(status_code=404, detail="Profession not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(p, k, v)
    session.add(p)
    session.commit()
    session.refresh(p)
    return p


@app.delete("/profession/{profession_id}", status_code=204)
def delete_profession(profession_id: int, session: Session = Depends(get_session)) -> None:
    p = session.get(Profession, profession_id)
    if not p:
        raise HTTPException(status_code=404, detail="Profession not found")
    session.delete(p)
    session.commit()


@app.get("/skills", response_model=list[SkillRead])
def list_skills(session: Session = Depends(get_session)) -> list[Skill]:
    return list(session.exec(select(Skill)).all())


@app.get("/skill/{skill_id}", response_model=SkillRead)
def get_skill(skill_id: int, session: Session = Depends(get_session)) -> Skill:
    s = session.get(Skill, skill_id)
    if not s:
        raise HTTPException(status_code=404, detail="Skill not found")
    return s


@app.post("/skill", response_model=SkillRead, status_code=201)
def create_skill(body: SkillCreate, session: Session = Depends(get_session)) -> Skill:
    s = Skill(**body.model_dump())
    session.add(s)
    session.commit()
    session.refresh(s)
    return s


@app.put("/skill/{skill_id}", response_model=SkillRead)
def update_skill(
    skill_id: int, body: SkillUpdate, session: Session = Depends(get_session)
) -> Skill:
    s = session.get(Skill, skill_id)
    if not s:
        raise HTTPException(status_code=404, detail="Skill not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(s, k, v)
    session.add(s)
    session.commit()
    session.refresh(s)
    return s


@app.delete("/skill/{skill_id}", status_code=204)
def delete_skill(skill_id: int, session: Session = Depends(get_session)) -> None:
    s = session.get(Skill, skill_id)
    if not s:
        raise HTTPException(status_code=404, detail="Skill not found")
    session.delete(s)
    session.commit()


@app.get("/warriors_list", response_model=list[WarriorShort])
def warriors_list(session: Session = Depends(get_session)) -> list[Warrior]:
    return list(session.exec(select(Warrior)).all())


@app.get("/warrior/{warrior_id}", response_model=WarriorRead)
def warriors_get(warrior_id: int, session: Session = Depends(get_session)) -> WarriorRead:
    stmt = (
        select(Warrior)
        .where(Warrior.id == warrior_id)
        .options(selectinload(Warrior.profession))
    )
    w = session.exec(stmt).first()
    if not w:
        raise HTTPException(status_code=404, detail="Warrior not found")
    return build_warrior_read(session, w)


@app.post("/warrior", response_model=WarriorShort, status_code=201)
def warriors_create(
    body: WarriorCreate, session: Session = Depends(get_session)
) -> Warrior:
    if not session.get(Profession, body.profession_id):
        raise HTTPException(status_code=400, detail="Profession not found")
    w = Warrior(**body.model_dump())
    session.add(w)
    session.commit()
    session.refresh(w)
    return w


@app.put("/warrior/{warrior_id}", response_model=WarriorShort)
def warrior_update(
    warrior_id: int, body: WarriorUpdate, session: Session = Depends(get_session)
) -> Warrior:
    w = session.get(Warrior, warrior_id)
    if not w:
        raise HTTPException(status_code=404, detail="Warrior not found")
    data = body.model_dump(exclude_unset=True)
    if "profession_id" in data and data["profession_id"] is not None:
        if not session.get(Profession, data["profession_id"]):
            raise HTTPException(status_code=400, detail="Profession not found")
    for k, v in data.items():
        setattr(w, k, v)
    session.add(w)
    session.commit()
    session.refresh(w)
    return w


@app.delete("/warrior/{warrior_id}", status_code=204)
def warrior_delete(warrior_id: int, session: Session = Depends(get_session)) -> None:
    w = session.get(Warrior, warrior_id)
    if not w:
        raise HTTPException(status_code=404, detail="Warrior not found")
    session.delete(w)
    session.commit()


@app.post("/warrior/{warrior_id}/skill/{skill_id}", status_code=201)
def link_skill_to_warrior(
    warrior_id: int,
    skill_id: int,
    session: Session = Depends(get_session),
    body: Annotated[Optional[SkillLinkBody], Body()] = None,
) -> dict:
    if not session.get(Warrior, warrior_id):
        raise HTTPException(status_code=404, detail="Warrior not found")
    if not session.get(Skill, skill_id):
        raise HTTPException(status_code=404, detail="Skill not found")
    existing = session.exec(
        select(SkillWarriorLink).where(
            SkillWarriorLink.warrior_id == warrior_id,
            SkillWarriorLink.skill_id == skill_id,
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Link already exists")
    lvl = body.level if body else None
    link = SkillWarriorLink(skill_id=skill_id, warrior_id=warrior_id, level=lvl)
    session.add(link)
    session.commit()
    return {"ok": True}


@app.delete("/warrior/{warrior_id}/skill/{skill_id}", status_code=204)
def unlink_skill_from_warrior(
    warrior_id: int, skill_id: int, session: Session = Depends(get_session)
) -> None:
    link = session.exec(
        select(SkillWarriorLink).where(
            SkillWarriorLink.warrior_id == warrior_id,
            SkillWarriorLink.skill_id == skill_id,
        )
    ).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    session.delete(link)
    session.commit()
