from typing import Generic, Optional, Type, TypeVar

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.models.postgres.models import Base

_M = TypeVar("_M", bound=Base)
_E = TypeVar("_E")


class BaseSQLAlchemyRepository(Generic[_M, _E]):
    def __init__(self, session: AsyncSession, model: Type[_M]):
        self.session = session
        self.model = model

    @staticmethod
    def to_entity(orm_model: _M) -> _E:
        return orm_model.to_entity()

    @staticmethod
    def to_dict(orm_model: _M) -> dict:
        return orm_model.to_dict()

    def from_entity(self, entity: _M) -> _M:
        return self.model.from_entity(entity)

    async def create(self, entity: _M) -> _E:
        orm_instance = self.from_entity(entity)
        self.session.add(orm_instance)
        await self.session.flush()
        return self.to_entity(orm_instance)

    async def update(self, entity: _M) -> _E:
        orm_instance = self.from_entity(entity)
        update_data = orm_instance.to_dict()
        update_data.pop("id", None)

        statement = (
            update(self.model)
            .where(self.model.id == orm_instance.id)
            .values(update_data)
            .returning(self.model)
        )
        result = await self.session.execute(statement)
        updated_orm_instance = result.scalar_one()
        return self.to_entity(updated_orm_instance)

    async def delete_by_id(self, entity_id: int) -> None:
        stmt = delete(self.model).where(self.model.id == entity_id)
        await self.session.execute(stmt)
