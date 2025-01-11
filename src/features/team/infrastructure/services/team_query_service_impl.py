from typing import Callable, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from features.team.domain.entities.team_query_model import TeamReadModel
from features.team.domain.services.team_query_service import TeamQueryService
from features.team.infrastructure.common.team_query_helper import SQLAlchemyTeamQueryHelper


class SQLAlchemyTeamQueryServiceImpl(TeamQueryService, SQLAlchemyTeamQueryHelper):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self.session_factory = session_factory

    async def fetch_all(self) -> Sequence[TeamReadModel]:
        async with self.session_factory() as session:
            teams = await self._fetch_all(session)
            return [team.to_read_model() for team in teams]

    async def fetch_by_id(self, id_: int) -> TeamReadModel | None:
        async with self.session_factory() as session:
            team = await self._fetch_by_id(session, id_)
            return team.to_read_model() if team else None

    async def fetch_all_with_user(self, user_id: int) -> Sequence[TeamReadModel]:
        async with self.session_factory() as session:
            teams = await self._fetch_all_with_user(session, user_id)
            return [team.to_read_model() for team in teams]
