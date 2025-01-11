from abc import ABC, abstractmethod
from typing import Sequence

from core.interfaces.query_service import BaseQueryService
from features.task.domain.entities.task_query_model import TaskReadModel
from features.team.domain.entities.team_query_model import TeamReadModel


class TaskQueryService(BaseQueryService[TaskReadModel], ABC):
    @abstractmethod
    async def fetch_all_by_team(self, team_id: int) -> Sequence[TaskReadModel]:
        ...

    @abstractmethod
    async def fetch_team_participants(self, team_id: int) -> Sequence[TeamReadModel]:
        ...
