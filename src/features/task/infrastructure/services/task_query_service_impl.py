from typing import Callable, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from features.task.domain.entities.task_query_model import TaskReadModel
from features.task.domain.services.task_query_service import TaskQueryService
from features.task.infrastructure.common.task_query_helper import SQLAlchemyTaskQueryHelper
from features.team.infrastructure.models.team_participants import team_participants
from features.user.domain.entities.user_query_model import UserReadModel
from features.user.infrastructure.models.user import User


class SQLAlchemyTaskQueryServiceImpl(TaskQueryService, SQLAlchemyTaskQueryHelper):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self.session_factory = session_factory

    async def fetch_all(self) -> Sequence[TaskReadModel]:
        async with self.session_factory() as session:
            tasks = await self._fetch_all(session)
            return [task.to_read_model() for task in tasks]

    async def fetch_by_id(self, id_: int) -> TaskReadModel | None:
        async with self.session_factory() as session:
            task = await self._fetch_by_id(session, id_)
            return task.to_read_model() if task else None

    async def fetch_all_by_team(self, team_id: int) -> Sequence[TaskReadModel]:
        async with self.session_factory() as session:
            tasks = await self._fetch_all_by_team(session, team_id)
            return [task.to_read_model() for task in tasks]

    async def fetch_team_participants(self, team_id: int) -> Sequence[UserReadModel]:
        async with self.session_factory() as session:
            query = (
                select(User)
                .join(team_participants, team_participants.c.user_id == User.id)
                .filter(team_participants.c.team_id == team_id)
            )

            result = await session.execute(query)
            participants = result.scalars().all()

            return [participant.to_read_model() for participant in participants]
