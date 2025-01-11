from typing import Callable, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from features.user.domain.entities.user_query_model import UserReadModel
from features.user.domain.services.user_query_service import UserQueryService
from features.user.infrastructure.common.user_query_helper import SQLAlchemyUserQueryHelper


class SQLAlchemyUserQueryServiceImpl(UserQueryService, SQLAlchemyUserQueryHelper):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self.session_factory = session_factory

    async def fetch_all(self) -> Sequence[UserReadModel]:
        async with self.session_factory() as session:
            users = await self._fetch_all(session)
            return [user.to_read_model() for user in users]

    async def fetch_by_id(self, id_: int) -> UserReadModel | None:
        async with self.session_factory() as session:
            user = await self._fetch_by_id(session, id_)
            return user.to_read_model() if user else None

    async def fetch_by_email(self, email: str) -> UserReadModel | None:
        async with self.session_factory() as session:
            user = await self._fetch_by_email(session, email)
            return user.to_read_model() if user else None
