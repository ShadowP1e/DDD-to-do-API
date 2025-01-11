from sqlalchemy.ext.asyncio import AsyncSession

from features.user.domain.repositories.user_repository import UserRepository
from features.user.domain.repositories.user_unit_of_work import UserUnitOfWork
from features.user.infrastructure.repositories.user_repository_impl import SQLAlchemyUserRepositoryImpl


class SQLAlchemyUserUnitOfWorkImpl(UserUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session
        self._user_repository: UserRepository | None = None

    @property
    def user_repository(self) -> UserRepository:
        if self._user_repository is None:
            self._user_repository = SQLAlchemyUserRepositoryImpl(self.session)
        return self._user_repository

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def close(self) -> None:
        await self.session.close()
