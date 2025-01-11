from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from features.user.infrastructure.models.user import User


class SQLAlchemyUserQueryHelper:
    """
    DRY for user repository and query service
    """

    @staticmethod
    async def _fetch_all(session: AsyncSession) -> Sequence[User]:
        query = select(User)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def _fetch_by_id(session: AsyncSession, id_: int) -> User | None:
        query = select(User).where(User.id == id_)
        result = await session.execute(query)
        try:
            return result.scalar_one()
        except NoResultFound:
            return None

    @staticmethod
    async def _fetch_by_email(session: AsyncSession, email: str) -> User | None:
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        try:
            return result.scalar_one()
        except NoResultFound:
            return None
