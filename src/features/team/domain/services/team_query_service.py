from abc import ABC, abstractmethod
from typing import Sequence

from core.interfaces.query_service import BaseQueryService
from features.team.domain.entities.team_query_model import TeamReadModel


class TeamQueryService(BaseQueryService[TeamReadModel], ABC):
    @abstractmethod
    async def fetch_all_with_user(self, user_id: int) -> Sequence[TeamReadModel]:
        ...
