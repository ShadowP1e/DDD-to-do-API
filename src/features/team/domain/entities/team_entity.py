import copy

from core.entities.base import BaseDomainEntity
from features.team.domain.actions.commands import CreateTeamCommand, UpdateTeamCommand
from features.team.domain.events.team_created import TeamCreatedEvent
from features.team.domain.events.team_updated import TeamUpdatedEvent
from features.user.domain.entities.user_entity import UserEntity


class TeamEntity(BaseDomainEntity):
    def __init__(
            self,
            id_: int | None,
            name: str,
            owner_id: int,
            owner: UserEntity | None = None,
            participants: list['UserEntity'] | None = None,
    ):
        super().__init__(id_=id_)
        self.name = name
        self.owner_id = owner_id
        self.owner = owner
        self.participants = participants or []

    def add_participant(self, user: 'UserEntity'):
        if user not in self.participants:
            self.participants.append(user)

    def remove_participant(self, user: 'UserEntity'):
        if user in self.participants:
            self.participants.remove(user)

    def change_owner(self, new_owner: 'UserEntity'):
        self.owner = new_owner

    @classmethod
    def create(cls, entity_create_model: 'CreateTeamCommand') -> 'TeamEntity':
        team = cls(
            id_=None,
            **entity_create_model.to_dict()
        )
        team.add_event(TeamCreatedEvent(team.id, team.name, team.owner_id))
        return team

    def update(self, entity_update_model: 'UpdateTeamCommand') -> 'TeamEntity':
        update_data = entity_update_model.to_dict()
        updated_team = copy.deepcopy(self)

        for attr_name, value in update_data.items():
            setattr(updated_team, attr_name, value)

        updated_team.add_event(TeamUpdatedEvent(self.id, self.name, self.owner_id))
        return updated_team

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TeamEntity):
            return self.id == other.id
        return False
