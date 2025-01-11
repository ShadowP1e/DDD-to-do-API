from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from features.team.infrastructure.models.team import Team
from features.user.infrastructure.models.user import User


class SQLAlchemyTeamQueryHelper:
    """
    DRY for team repository and query service
    """

    @staticmethod
    async def _fetch_all(session: AsyncSession) -> Sequence[Team]:
        query = select(Team).options(
            joinedload(Team.owner),
            selectinload(Team.participants)
        )
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def _fetch_by_id(session: AsyncSession, id_: int) -> Team | None:
        query = select(Team).options(
            joinedload(Team.owner),
            selectinload(Team.participants)
        ).filter(Team.id == id_)
        result = await session.execute(query)
        team = result.scalar_one_or_none()

        if team is None:
            return None

        return team

    @staticmethod
    async def _fetch_all_with_user(session: AsyncSession, user_id: int) -> Sequence[Team]:
        query = (
            select(Team)
            .options(
                joinedload(Team.owner),
                selectinload(Team.participants)
            )
            .filter(Team.participants.any(User.id == user_id))
        )
        result = await session.execute(query)
        teams = result.scalars().all()
        return teams
