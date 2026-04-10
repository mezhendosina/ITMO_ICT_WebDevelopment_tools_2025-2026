from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.database import get_session
from app.api.auth import get_current_user
from app.models.team import Team, TeamCreate, TeamUpdate, TeamRead
from app.services.team_service import TeamService

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.get("", response_model=list[TeamRead])
def read_teams(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    team_service = TeamService(session)
    return team_service.get_all(skip=skip, limit=limit)


@router.get("/hackathon/{hackathon_id}", response_model=list[TeamRead])
def read_teams_by_hackathon(hackathon_id: int, session: Session = Depends(get_session)):
    team_service = TeamService(session)
    return team_service.get_by_hackathon(hackathon_id)


@router.get("/creator/{creator_id}", response_model=list[TeamRead])
def read_teams_by_creator(creator_id: int, session: Session = Depends(get_session)):
    team_service = TeamService(session)
    return team_service.get_by_creator(creator_id)


@router.get("/{team_id}/members")
def read_team_members(team_id: int, session: Session = Depends(get_session)):
    team_service = TeamService(session)
    team = team_service.get_with_members(team_id)

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )

    return team.members


@router.get("/{team_id}", response_model=TeamRead)
def read_team(team_id: int, session: Session = Depends(get_session)):
    team_service = TeamService(session)
    team = team_service.get_by_id(team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )
    return team


@router.post("", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
def create_team(
    team_create: TeamCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    team_service = TeamService(session)
    return team_service.create(team_create, current_user.id)


@router.patch("/{team_id}", response_model=TeamRead)
def update_team(
    team_id: int,
    team_update: TeamUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    team_service = TeamService(session)
    team = team_service.get_by_id(team_id)

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )

    if team.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this team",
        )

    updated_team = team_service.update(team_id, team_update)
    return updated_team


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(
    team_id: int,
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    team_service = TeamService(session)
    team = team_service.get_by_id(team_id)

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )

    if team.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this team",
        )

    team_service.delete(team_id)
