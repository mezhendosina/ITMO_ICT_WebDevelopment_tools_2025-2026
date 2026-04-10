from fastapi import FastAPI, HTTPException
from typing_extensions import TypedDict

from models import Profession, RaceType, Skill, Warrior

app = FastAPI(title="Практика 1.1 — воины (временная БД)")


class WarriorCreateResponse(TypedDict):
    status: int
    data: Warrior


temp_professions: list[dict] = [
    {
        "id": 1,
        "title": "Влиятельный человек",
        "description": "Эксперт по всем вопросам",
    },
    {
        "id": 2,
        "title": "Дельфист-гребец",
        "description": "Уважаемый сотрудник",
    },
]

temp_bd: list[dict] = [
    {
        "id": 1,
        "race": "director",
        "name": "Мартынов Дмитрий",
        "level": 12,
        "profession": {
            "id": 1,
            "title": "Влиятельный человек",
            "description": "Эксперт по всем вопросам",
        },
        "skills": [
            {
                "id": 1,
                "name": "Купле-продажа компрессоров",
                "description": "",
            },
            {
                "id": 2,
                "name": "Оценка имущества",
                "description": "",
            },
        ],
    },
    {
        "id": 2,
        "race": "worker",
        "name": "Андрей Косякин",
        "level": 12,
        "profession": {
            "id": 1,
            "title": "Дельфист-гребец",
            "description": "Уважаемый сотрудник",
        },
        "skills": [],
    },
]


@app.get("/")
def hello() -> str:
    return "Hello, warrior!"


@app.get("/warriors_list", response_model=list[Warrior])
def warriors_list() -> list[dict]:
    return temp_bd


@app.get("/warrior/{warrior_id}", response_model=list[Warrior])
def warriors_get(warrior_id: int) -> list[dict]:
    return [w for w in temp_bd if w.get("id") == warrior_id]


@app.post("/warrior", response_model=WarriorCreateResponse)
def warriors_create(warrior: Warrior) -> WarriorCreateResponse:
    warrior_to_append = warrior.model_dump()
    temp_bd.append(warrior_to_append)
    return {"status": 200, "data": warrior}


@app.delete("/warrior/{warrior_id}")
def warrior_delete(warrior_id: int) -> dict:
    for i, warrior in enumerate(temp_bd):
        if warrior.get("id") == warrior_id:
            temp_bd.pop(i)
            return {"status": 201, "message": "deleted"}
    raise HTTPException(status_code=404, detail="Warrior not found")


@app.put("/warrior/{warrior_id}", response_model=list[Warrior])
def warrior_update(warrior_id: int, warrior: Warrior) -> list[dict]:
    found = False
    for i, war in enumerate(temp_bd):
        if war.get("id") == warrior_id:
            temp_bd[i] = warrior.model_dump()
            found = True
            break
    if not found:
        raise HTTPException(status_code=404, detail="Warrior not found")
    return temp_bd


@app.get("/professions", response_model=list[Profession])
def professions_list() -> list[dict]:
    return temp_professions


@app.get("/profession/{profession_id}", response_model=Profession)
def profession_get(profession_id: int) -> dict:
    for p in temp_professions:
        if p.get("id") == profession_id:
            return p
    raise HTTPException(status_code=404, detail="Profession not found")


@app.post("/profession", response_model=Profession, status_code=201)
def profession_create(profession: Profession) -> dict:
    if any(p.get("id") == profession.id for p in temp_professions):
        raise HTTPException(status_code=400, detail="Profession id already exists")
    data = profession.model_dump()
    temp_professions.append(data)
    return data


@app.put("/profession/{profession_id}", response_model=Profession)
def profession_update(profession_id: int, profession: Profession) -> dict:
    if profession.id != profession_id:
        raise HTTPException(status_code=400, detail="Path id and body id must match")
    for i, p in enumerate(temp_professions):
        if p.get("id") == profession_id:
            temp_professions[i] = profession.model_dump()
            return temp_professions[i]
    raise HTTPException(status_code=404, detail="Profession not found")


@app.delete("/profession/{profession_id}")
def profession_delete(profession_id: int) -> dict:
    for i, p in enumerate(temp_professions):
        if p.get("id") == profession_id:
            temp_professions.pop(i)
            return {"status": 200, "message": "deleted"}
    raise HTTPException(status_code=404, detail="Profession not found")
