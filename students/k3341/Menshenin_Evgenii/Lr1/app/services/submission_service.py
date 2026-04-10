from typing import List, Optional
from sqlmodel import Session, select
from app.models.submission import Submission, SubmissionCreate, SubmissionUpdate


class SubmissionService:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Submission]:
        statement = select(Submission).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def get_by_id(self, submission_id: int) -> Optional[Submission]:
        return self.session.get(Submission, submission_id)

    def get_by_user(self, user_id: int) -> List[Submission]:
        statement = select(Submission).where(Submission.user_id == user_id)
        return list(self.session.exec(statement).all())

    def get_by_task(self, task_id: int) -> List[Submission]:
        statement = select(Submission).where(Submission.task_id == task_id)
        return list(self.session.exec(statement).all())

    def get_by_team(self, team_id: int) -> List[Submission]:
        statement = select(Submission).where(Submission.team_id == team_id)
        return list(self.session.exec(statement).all())

    def create(self, submission_create: SubmissionCreate, user_id: int) -> Submission:
        submission = Submission(**submission_create.model_dump(), user_id=user_id)
        self.session.add(submission)
        self.session.commit()
        self.session.refresh(submission)
        return submission

    def update(
        self, submission_id: int, submission_update: SubmissionUpdate
    ) -> Optional[Submission]:
        submission = self.get_by_id(submission_id)
        if not submission:
            return None

        update_data = submission_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(submission, key, value)

        self.session.add(submission)
        self.session.commit()
        self.session.refresh(submission)
        return submission

    def delete(self, submission_id: int) -> bool:
        submission = self.get_by_id(submission_id)
        if not submission:
            return False

        self.session.delete(submission)
        self.session.commit()
        return True
