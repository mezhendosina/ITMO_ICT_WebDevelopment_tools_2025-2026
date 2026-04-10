from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.database import get_session
from app.api.auth import get_current_user
from app.models.submission import (
    Submission,
    SubmissionCreate,
    SubmissionUpdate,
    SubmissionRead,
)
from app.services.submission_service import SubmissionService

router = APIRouter(prefix="/submissions", tags=["Submissions"])


@router.get("", response_model=list[SubmissionRead])
def read_submissions(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    submission_service = SubmissionService(session)
    return submission_service.get_all(skip=skip, limit=limit)


@router.get("/user/{user_id}", response_model=list[SubmissionRead])
def read_submissions_by_user(user_id: int, session: Session = Depends(get_session)):
    submission_service = SubmissionService(session)
    return submission_service.get_by_user(user_id)


@router.get("/task/{task_id}", response_model=list[SubmissionRead])
def read_submissions_by_task(task_id: int, session: Session = Depends(get_session)):
    submission_service = SubmissionService(session)
    return submission_service.get_by_task(task_id)


@router.get("/team/{team_id}", response_model=list[SubmissionRead])
def read_submissions_by_team(team_id: int, session: Session = Depends(get_session)):
    submission_service = SubmissionService(session)
    return submission_service.get_by_team(team_id)


@router.get("/{submission_id}", response_model=SubmissionRead)
def read_submission(submission_id: int, session: Session = Depends(get_session)):
    submission_service = SubmissionService(session)
    submission = submission_service.get_by_id(submission_id)
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found"
        )
    return submission


@router.post("", response_model=SubmissionRead, status_code=status.HTTP_201_CREATED)
def create_submission(
    submission_create: SubmissionCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    submission_service = SubmissionService(session)
    return submission_service.create(submission_create, current_user.id)


@router.patch("/{submission_id}", response_model=SubmissionRead)
def update_submission(
    submission_id: int,
    submission_update: SubmissionUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    submission_service = SubmissionService(session)
    submission = submission_service.get_by_id(submission_id)

    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found"
        )

    if submission.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this submission",
        )

    updated_submission = submission_service.update(submission_id, submission_update)
    return updated_submission


@router.delete("/{submission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_submission(
    submission_id: int,
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    submission_service = SubmissionService(session)
    submission = submission_service.get_by_id(submission_id)

    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found"
        )

    if submission.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this submission",
        )

    submission_service.delete(submission_id)
