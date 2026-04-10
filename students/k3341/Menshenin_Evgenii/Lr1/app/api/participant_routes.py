from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.database import get_session
from app.api.auth import get_current_user
from app.models.participant import (
    Participant,
    ParticipantCreate,
    ParticipantUpdate,
    ParticipantRead,
)
from app.services.participant_service import ParticipantService

router = APIRouter(prefix="/participants", tags=["Participants"])


@router.get("", response_model=list[ParticipantRead])
def read_participants(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    participant_service = ParticipantService(session)
    return participant_service.get_all(skip=skip, limit=limit)


@router.get("/user/{user_id}", response_model=list[ParticipantRead])
def read_participants_by_user(user_id: int, session: Session = Depends(get_session)):
    participant_service = ParticipantService(session)
    return participant_service.get_by_user(user_id)


@router.get("/hackathon/{hackathon_id}", response_model=list[ParticipantRead])
def read_participants_by_hackathon(
    hackathon_id: int, session: Session = Depends(get_session)
):
    participant_service = ParticipantService(session)
    return participant_service.get_by_hackathon(hackathon_id)


@router.get("/{participant_id}", response_model=ParticipantRead)
def read_participant(participant_id: int, session: Session = Depends(get_session)):
    participant_service = ParticipantService(session)
    participant = participant_service.get_by_id(participant_id)
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Participant not found"
        )
    return participant


@router.post("", response_model=ParticipantRead, status_code=status.HTTP_201_CREATED)
def create_participant(
    participant_create: ParticipantCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    participant_service = ParticipantService(session)
    return participant_service.create(participant_create)


@router.patch("/{participant_id}", response_model=ParticipantRead)
def update_participant(
    participant_id: int,
    participant_update: ParticipantUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    participant_service = ParticipantService(session)
    updated_participant = participant_service.update(participant_id, participant_update)

    if not updated_participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Participant not found"
        )

    return updated_participant


@router.delete("/{participant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_participant(
    participant_id: int,
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    participant_service = ParticipantService(session)
    success = participant_service.delete(participant_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Participant not found"
        )
