from typing import List, Optional
from sqlmodel import Session, select
from app.models.participant import Participant, ParticipantCreate, ParticipantUpdate


class ParticipantService:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Participant]:
        statement = select(Participant).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def get_by_id(self, participant_id: int) -> Optional[Participant]:
        return self.session.get(Participant, participant_id)

    def get_by_user(self, user_id: int) -> List[Participant]:
        statement = select(Participant).where(Participant.user_id == user_id)
        return list(self.session.exec(statement).all())

    def get_by_hackathon(self, hackathon_id: int) -> List[Participant]:
        statement = select(Participant).where(Participant.hackathon_id == hackathon_id)
        return list(self.session.exec(statement).all())

    def create(self, participant_create: ParticipantCreate) -> Participant:
        participant = Participant(**participant_create.model_dump())
        self.session.add(participant)
        self.session.commit()
        self.session.refresh(participant)
        return participant

    def update(
        self, participant_id: int, participant_update: ParticipantUpdate
    ) -> Optional[Participant]:
        participant = self.get_by_id(participant_id)
        if not participant:
            return None

        update_data = participant_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(participant, key, value)

        self.session.add(participant)
        self.session.commit()
        self.session.refresh(participant)
        return participant

    def delete(self, participant_id: int) -> bool:
        participant = self.get_by_id(participant_id)
        if not participant:
            return False

        self.session.delete(participant)
        self.session.commit()
        return True
