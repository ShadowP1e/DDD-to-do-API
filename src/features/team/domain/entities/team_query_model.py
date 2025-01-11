from dataclasses import dataclass

from features.team.domain.entities.team_entity import TeamEntity
from features.user.domain.entities.user_query_model import UserReadModel


@dataclass
class TeamReadModel:
    id: int
    name: str
    owner_id: int
    owner: UserReadModel
    participants: list[UserReadModel]

    @classmethod
    def from_entity(cls, entity: TeamEntity) -> 'TeamReadModel':
        return cls(
            id=entity.id,
            name=entity.name,
            owner_id=entity.owner_id,
            owner=UserReadModel.from_entity(entity.owner),
            participants=[UserReadModel.from_entity(participant) for participant in entity.participants]
        )
