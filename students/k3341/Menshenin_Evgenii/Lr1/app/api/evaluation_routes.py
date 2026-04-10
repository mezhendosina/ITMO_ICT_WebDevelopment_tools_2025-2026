from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.database import get_session
from app.api.auth import get_current_user
from app.models.evaluation import (
    Evaluation,
    EvaluationCreate,
    EvaluationUpdate,
    EvaluationRead,
)
from app.services.evaluation_service import EvaluationService

router = APIRouter(prefix="/evaluations", tags=["Evaluations"])


@router.get("", response_model=list[EvaluationRead])
def read_evaluations(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    evaluation_service = EvaluationService(session)
    return evaluation_service.get_all(skip=skip, limit=limit)


@router.get("/submission/{submission_id}", response_model=list[EvaluationRead])
def read_evaluations_by_submission(
    submission_id: int, session: Session = Depends(get_session)
):
    evaluation_service = EvaluationService(session)
    return evaluation_service.get_by_submission(submission_id)


@router.get("/evaluator/{evaluator_id}", response_model=list[EvaluationRead])
def read_evaluations_by_evaluator(
    evaluator_id: int, session: Session = Depends(get_session)
):
    evaluation_service = EvaluationService(session)
    return evaluation_service.get_by_evaluator(evaluator_id)


@router.get("/{evaluation_id}", response_model=EvaluationRead)
def read_evaluation(evaluation_id: int, session: Session = Depends(get_session)):
    evaluation_service = EvaluationService(session)
    evaluation = evaluation_service.get_by_id(evaluation_id)
    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found"
        )
    return evaluation


@router.post("", response_model=EvaluationRead, status_code=status.HTTP_201_CREATED)
def create_evaluation(
    evaluation_create: EvaluationCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    evaluation_service = EvaluationService(session)
    return evaluation_service.create(evaluation_create, current_user.id)


@router.patch("/{evaluation_id}", response_model=EvaluationRead)
def update_evaluation(
    evaluation_id: int,
    evaluation_update: EvaluationUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    evaluation_service = EvaluationService(session)
    evaluation = evaluation_service.get_by_id(evaluation_id)

    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found"
        )

    if evaluation.evaluator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this evaluation",
        )

    updated_evaluation = evaluation_service.update(evaluation_id, evaluation_update)
    return updated_evaluation


@router.delete("/{evaluation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_evaluation(
    evaluation_id: int,
    current_user: Annotated[dict, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    evaluation_service = EvaluationService(session)
    evaluation = evaluation_service.get_by_id(evaluation_id)

    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found"
        )

    if evaluation.evaluator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this evaluation",
        )

    evaluation_service.delete(evaluation_id)
