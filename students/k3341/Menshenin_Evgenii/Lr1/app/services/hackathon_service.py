from typing import List, Optional
from sqlmodel import Session, select
from app.models.hackathon import Hackathon, HackathonCreate, HackathonUpdate


class HackathonService:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Hackathon]:
        statement = select(Hackathon).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def get_by_id(self, hackathon_id: int) -> Optional[Hackathon]:
        return self.session.get(Hackathon, hackathon_id)

    def get_by_organizer(self, organizer_id: int) -> List[Hackathon]:
        statement = select(Hackathon).where(Hackathon.organizer_id == organizer_id)
        return list(self.session.exec(statement).all())

    def create(self, hackathon_create: HackathonCreate, organizer_id: int) -> Hackathon:
        hackathon = Hackathon(
            **hackathon_create.model_dump(), organizer_id=organizer_id
        )
        self.session.add(hackathon)
        self.session.commit()
        self.session.refresh(hackathon)
        return hackathon

    def update(
        self, hackathon_id: int, hackathon_update: HackathonUpdate
    ) -> Optional[Hackathon]:
        hackathon = self.get_by_id(hackathon_id)
        if not hackathon:
            return None

        update_data = hackathon_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(hackathon, key, value)

        self.session.add(hackathon)
        self.session.commit()
        self.session.refresh(hackathon)
        return hackathon

    def delete(self, hackathon_id: int) -> bool:
        hackathon = self.get_by_id(hackathon_id)
        if not hackathon:
            return False

        self.session.delete(hackathon)
        self.session.commit()
        return True

    def get_with_participants(self, hackathon_id: int) -> Optional[Hackathon]:
        hackathon = self.get_by_id(hackathon_id)
        if hackathon:
            self.session.refresh(hackathon, attribute_names=["participants"])
        return hackathon

    def get_with_tasks(self, hackathon_id: int) -> Optional[Hackathon]:
        hackathon = self.get_by_id(hackathon_id)
        if hackathon:
            self.session.refresh(hackathon, attribute_names=["tasks"])
        return hackathon
