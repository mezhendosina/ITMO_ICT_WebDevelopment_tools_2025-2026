from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.database import get_session
from app.api.auth import get_current_user
from app.models.hackathon import (
    Hackathon,
    HackathonCreate,
    HackathonUpdate,
    HackathonRead,
)
from app.services.hackathon_service import HackathonService

router = APIRouter(prefix="/hackathons", tags=["Hackathons"])


@router.get("", response_model=list[HackathonRead])
def read_hackathons(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    hackathon_service = HackathonService(session)
    return hackathon_service.get_all(skip=skip, limit=limit)


@router.get("/{hackathon_id}", response_model=HackathonRead)
def read_hackathon(hackathon_id: int, session: Session = Depends(get_session)):
    hackathon_service = HackathonService(session)
    hackathon = hackathon_service.get_by_id(hackathon_id)
    if not hackathon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hackathon not found"
        )
    return hackathon


@router.post("", response_model=HackathonRead, status_code=status.HTTP_201_CREATED)
def create_hackathon(
    hackathon_create: HackathonCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    hackathon_service = HackathonService(session)
    return hackathon_service.create(hackathon_create, current_user.id)


@router.patch("/{hackathon_id}", response_model=HackathonRead)
def update_hackathon(
    hackathon_id: int,
    hackathon_update: HackathonUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    hackathon_service = HackathonService(session)
    hackathon = hackathon_service.get_by_id(hackathon_id)

    if not hackathon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hackathon not found"
        )

    if hackathon.organizer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this hackathon",
        )

    updated_hackathon = hackathon_service.update(hackathon_id, hackathon_update)
    return updated_hackathon


@router.delete("/{hackathon_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hackathon(
    hackathon_id: int,
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    hackathon_service = HackathonService(session)
    hackathon = hackathon_service.get_by_id(hackathon_id)

    if not hackathon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hackathon not found"
        )

    if hackathon.organizer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this hackathon",
        )

    hackathon_service.delete(hackathon_id)


@router.get("/{hackathon_id}/participants")
def read_hackathon_participants(
    hackathon_id: int, session: Session = Depends(get_session)
):
    hackathon_service = HackathonService(session)
    hackathon = hackathon_service.get_with_participants(hackathon_id)

    if not hackathon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hackathon not found"
        )

    return hackathon.participants


@router.get("/{hackathon_id}/tasks")
def read_hackathon_tasks(hackathon_id: int, session: Session = Depends(get_session)):
    hackathon_service = HackathonService(session)
    hackathon = hackathon_service.get_with_tasks(hackathon_id)

    if not hackathon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hackathon not found"
        )

    return hackathon.tasks
