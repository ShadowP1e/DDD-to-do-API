from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.postgres.models import Base
from features.team.domain.entities.team_entity import TeamEntity
from features.team.domain.entities.team_query_model import TeamReadModel
from features.team.infrastructure.models.team_participants import team_participants
from features.user.infrastructure.models.user import User


class Team(Base):
    __tablename__ = 'teams'

    name: Mapped[str] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    owner: Mapped[User] = relationship("User", foreign_keys=[owner_id], lazy='joined')
    participants: Mapped[list[User]] = relationship(
        "User",
        secondary=team_participants,
        lazy='selectin',
    )

    def to_entity(self) -> 'TeamEntity':
        return TeamEntity(
            id_=self.id,
            name=self.name,
            owner_id=self.owner_id,
            owner=self.owner.to_entity(),
            participants=[participant.to_entity() for participant in self.participants],
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'owner_id': self.owner_id,
            'owner': self.owner.to_dict() if self.owner else None,
            'participants': [participant.to_dict() for participant in self.participants],
        }

    def to_read_model(self) -> 'TeamReadModel':
        return TeamReadModel(
            id=self.id,
            name=self.name,
            owner_id=self.owner_id,
            owner=self.owner.to_read_model() if self.owner else None,
            participants=[participant.to_read_model() for participant in self.participants],
        )

    @classmethod
    def from_entity(cls, team: 'TeamEntity') -> 'Team':
        return cls(
            id=team.id,
            name=team.name,
            owner_id=team.owner_id,
            owner=User.from_entity(team.owner) if team.owner else None,
            participants=[
                User.from_entity(participant) for participant in team.participants
            ],
        )
