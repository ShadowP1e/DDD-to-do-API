from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from features.task.infrastructure.models.task import Task


class SQLAlchemyTaskQueryHelper:
    """
    DRY for task repository and query service
    """

    @staticmethod
    async def _fetch_all(session: AsyncSession) -> Sequence[Task]:
        query = select(Task).options(
            joinedload(Task.team),
            joinedload(Task.creator),
            joinedload(Task.assignee),
        )
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def _fetch_by_id(session: AsyncSession, id_: int) -> Task | None:
        query = select(Task).options(
            joinedload(Task.team),
            joinedload(Task.creator),
            joinedload(Task.assignee),
        ).filter(Task.id == id_)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if task is None:
            return None

        return task

    @staticmethod
    async def _fetch_all_by_team(session: AsyncSession, team_id: int) -> Sequence[Task]:
        query = select(Task).options(
            joinedload(Task.team),
            joinedload(Task.creator),
            joinedload(Task.assignee),
        ).filter(Task.team_id == team_id)
        result = await session.execute(query)
        return result.scalars().all()
