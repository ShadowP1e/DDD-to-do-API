from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories.base import BaseSQLAlchemyRepository
from features.task.domain.entities.task_entity import TaskEntity
from features.task.domain.repositories.task_repository import TaskRepository
from features.task.infrastructure.common.task_query_helper import SQLAlchemyTaskQueryHelper
from features.task.infrastructure.models.task import Task
from features.user.infrastructure.models.user import User
from features.team.infrastructure.models.team import Team


class SQLAlchemyTaskRepositoryImpl(
    BaseSQLAlchemyRepository[Task, TaskEntity],
    SQLAlchemyTaskQueryHelper,
    TaskRepository,
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Task)

    async def create(self, entity: TaskEntity) -> TaskEntity:
        task = Task.from_entity(entity)

        await self._set_team_for_task(task, entity.team_id)
        await self._set_creator_for_task(task, entity.creator_id)

        self.session.add(task)
        await self.session.flush()

        return task.to_entity()

    async def update(self, entity: TaskEntity) -> TaskEntity:
        task = await self._fetch_by_id(self.session, entity.id)

        task.title = entity.title
        task.description = entity.description
        task.team_id = entity.team_id
        task.creator_id = entity.creator_id
        task.assignee_id = entity.assignee_id
        task.deadline = entity.deadline

        await self._set_team_for_task(task, entity.team_id)
        await self._set_creator_for_task(task, entity.creator_id)
        await self._set_assignee_for_task(task, entity.assignee_id)

        self.session.add(task)
        await self.session.flush()

        return task.to_entity()

    async def fetch_all(self) -> Sequence[TaskEntity]:
        tasks = await self._fetch_all(self.session)
        return [task.to_entity() for task in tasks]

    async def fetch_by_id(self, id_: int) -> TaskEntity | None:
        task = await self._fetch_by_id(self.session, id_)
        return task.to_entity() if task else None

    async def fetch_all_by_team(self, team_id: int) -> Sequence[TaskEntity]:
        tasks = await self._fetch_all_by_team(self.session, team_id)
        return [task.to_entity() for task in tasks]

    async def _set_team_for_task(self, task: Task, team_id: int | None) -> None:
        if team_id:
            team = await self.session.execute(select(Team).filter_by(id=team_id))
            team = team.scalar_one_or_none()
            if not team:
                raise ValueError(f"Team with ID {team_id} does not exist.")
            task.team = team

    async def _set_creator_for_task(self, task: Task, creator_id: int | None) -> None:
        if creator_id:
            creator = await self.session.execute(select(User).filter_by(id=creator_id))
            creator = creator.scalar_one_or_none()
            if not creator:
                raise ValueError(f"Creator with ID {creator_id} does not exist.")
            task.creator = creator

    async def _set_assignee_for_task(self, task: Task, assignee_id: int | None) -> None:
        if assignee_id:
            assignee = await self.session.execute(select(User).filter_by(id=assignee_id))
            assignee = assignee.scalar_one_or_none()
            if not assignee:
                raise ValueError(f"Assignee with ID {assignee_id} does not exist.")
            task.assignee = assignee
