from abc import ABC

from core.interfaces.repository import BaseRepository
from features.team.domain.entities.team_entity import TeamEntity


class TeamRepository(BaseRepository[TeamEntity], ABC):
    ...
