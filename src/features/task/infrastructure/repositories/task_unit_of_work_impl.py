from sqlalchemy.ext.asyncio import AsyncSession

from features.task.domain.repositories.task_repository import TaskRepository
from features.task.domain.repositories.task_unit_of_work import TaskUnitOfWork
from features.task.infrastructure.repositories.task_repository_impl import SQLAlchemyTaskRepositoryImpl
from features.team.domain.repositories.team_repository import TeamRepository
from features.team.infrastructure.repositories.team_repository_impl import SQLAlchemyTeamRepositoryImpl
from features.user.domain.repositories.user_repository import UserRepository
from features.user.infrastructure.repositories.user_repository_impl import SQLAlchemyUserRepositoryImpl


class SQLAlchemyTaskUnitOfWorkImpl(TaskUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session
        self._user_repository: UserRepository | None = None
        self._team_repository: TeamRepository | None = None
        self._task_repository: TaskRepository | None = None

    @property
    def user_repository(self) -> UserRepository:
        if self._user_repository is None:
            self._user_repository = SQLAlchemyUserRepositoryImpl(self.session)
        return self._user_repository

    @property
    def team_repository(self) -> TeamRepository:
        if self._team_repository is None:
            self._team_repository = SQLAlchemyTeamRepositoryImpl(self.session)
        return self._team_repository

    @property
    def task_repository(self) -> TaskRepository:
        if self._task_repository is None:
            self._task_repository = SQLAlchemyTaskRepositoryImpl(self.session)
        return self._task_repository

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def close(self) -> None:
        await self.session.close()
