from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories.base import BaseSQLAlchemyRepository
from features.user.domain.entities.user_entity import UserEntity
from features.user.domain.repositories.user_repository import UserRepository
from features.user.infrastructure.common.user_query_helper import SQLAlchemyUserQueryHelper
from features.user.infrastructure.models.user import User


class SQLAlchemyUserRepositoryImpl(
    BaseSQLAlchemyRepository[User, UserEntity],
    SQLAlchemyUserQueryHelper,
    UserRepository,
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def fetch_all(self) -> Sequence[UserEntity]:
        users = await self._fetch_all(self.session)
        return [user.to_entity() for user in users]

    async def fetch_by_id(self, id_: int) -> UserEntity | None:
        user = await self._fetch_by_id(self.session, id_)
        return user.to_entity() if user else None

    async def fetch_by_email(self, email: str) -> UserEntity | None:
        user = await self._fetch_by_email(self.session, email)
        return user.to_entity() if user else None
