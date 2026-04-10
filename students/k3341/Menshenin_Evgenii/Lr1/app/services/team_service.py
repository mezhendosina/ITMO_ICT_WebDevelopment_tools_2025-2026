from typing import List, Optional
from sqlmodel import Session, select
from app.models.team import Team, TeamCreate, TeamUpdate


class TeamService:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Team]:
        statement = select(Team).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def get_by_id(self, team_id: int) -> Optional[Team]:
        return self.session.get(Team, team_id)

    def get_by_hackathon(self, hackathon_id: int) -> List[Team]:
        statement = select(Team).where(Team.hackathon_id == hackathon_id)
        return list(self.session.exec(statement).all())

    def get_by_creator(self, creator_id: int) -> List[Team]:
        statement = select(Team).where(Team.creator_id == creator_id)
        return list(self.session.exec(statement).all())

    def create(self, team_create: TeamCreate, creator_id: int) -> Team:
        team = Team(**team_create.model_dump(), creator_id=creator_id)
        self.session.add(team)
        self.session.commit()
        self.session.refresh(team)
        return team

    def update(self, team_id: int, team_update: TeamUpdate) -> Optional[Team]:
        team = self.get_by_id(team_id)
        if not team:
            return None

        update_data = team_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(team, key, value)

        self.session.add(team)
        self.session.commit()
        self.session.refresh(team)
        return team

    def delete(self, team_id: int) -> bool:
        team = self.get_by_id(team_id)
        if not team:
            return False

        self.session.delete(team)
        self.session.commit()
        return True

    def get_with_members(self, team_id: int) -> Optional[Team]:
        team = self.get_by_id(team_id)
        if team:
            self.session.refresh(team, attribute_names=["members"])
        return team
