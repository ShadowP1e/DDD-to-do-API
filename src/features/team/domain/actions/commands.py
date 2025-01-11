from dataclasses import dataclass

from core.actions.base import BaseAction


@dataclass
class CreateTeamCommand(BaseAction):
    name: str
    owner_id: int


@dataclass
class UpdateTeamCommand(BaseAction):
    name: str | None = None
    owner_id: int | None = None


@dataclass
class AddParticipantTeamCommand(BaseAction):
    team_id: int
    user_id: int
    current_user_id: int


@dataclass
class RemoveParticipantTeamCommand(BaseAction):
    team_id: int
    user_id: int
    current_user_id: int


@dataclass
class DeleteTeamCommand(BaseAction):
    team_id: int
    current_user_id: int
