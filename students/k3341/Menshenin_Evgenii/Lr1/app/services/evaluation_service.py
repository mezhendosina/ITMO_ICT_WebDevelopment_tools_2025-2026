from typing import List, Optional
from sqlmodel import Session, select
from app.models.evaluation import Evaluation, EvaluationCreate, EvaluationUpdate


class EvaluationService:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Evaluation]:
        statement = select(Evaluation).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def get_by_id(self, evaluation_id: int) -> Optional[Evaluation]:
        return self.session.get(Evaluation, evaluation_id)

    def get_by_submission(self, submission_id: int) -> List[Evaluation]:
        statement = select(Evaluation).where(Evaluation.submission_id == submission_id)
        return list(self.session.exec(statement).all())

    def get_by_evaluator(self, evaluator_id: int) -> List[Evaluation]:
        statement = select(Evaluation).where(Evaluation.evaluator_id == evaluator_id)
        return list(self.session.exec(statement).all())

    def create(
        self, evaluation_create: EvaluationCreate, evaluator_id: int
    ) -> Evaluation:
        evaluation = Evaluation(
            **evaluation_create.model_dump(), evaluator_id=evaluator_id
        )
        self.session.add(evaluation)
        self.session.commit()
        self.session.refresh(evaluation)
        return evaluation

    def update(
        self, evaluation_id: int, evaluation_update: EvaluationUpdate
    ) -> Optional[Evaluation]:
        evaluation = self.get_by_id(evaluation_id)
        if not evaluation:
            return None

        update_data = evaluation_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(evaluation, key, value)

        self.session.add(evaluation)
        self.session.commit()
        self.session.refresh(evaluation)
        return evaluation

    def delete(self, evaluation_id: int) -> bool:
        evaluation = self.get_by_id(evaluation_id)
        if not evaluation:
            return False

        self.session.delete(evaluation)
        self.session.commit()
        return True
