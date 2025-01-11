from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories.base import BaseSQLAlchemyRepository
from features.team.domain.entities.team_entity import TeamEntity
from features.team.domain.repositories.team_repository import TeamRepository
from features.team.infrastructure.common.team_query_helper import SQLAlchemyTeamQueryHelper
from features.team.infrastructure.models.team import Team
from features.user.infrastructure.models.user import User


class SQLAlchemyTeamRepositoryImpl(
    BaseSQLAlchemyRepository[Team, TeamEntity],
    SQLAlchemyTeamQueryHelper,
    TeamRepository,
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Team)

    async def create(self, entity: TeamEntity) -> TeamEntity:
        team = Team.from_entity(entity)

        if team.owner_id:
            owner = await self.session.execute(select(User).filter_by(id=team.owner_id))
            owner = owner.scalar_one_or_none()

            if not owner:
                raise ValueError(f"Owner with ID {team.owner_id} does not exist.")
            team.owner = owner
            team.participants = [owner]

        self.session.add(team)
        await self.session.flush()

        return team.to_entity()

    async def update(self, entity: TeamEntity) -> TeamEntity:
        team = await self._fetch_by_id(self.session, entity.id)

        team.name = entity.name
        team.owner_id = entity.owner_id

        new_participant_ids = {user.id for user in entity.participants}
        current_participant_ids = {user.id for user in team.participants}

        to_add_ids = new_participant_ids - current_participant_ids
        to_remove_ids = current_participant_ids - new_participant_ids

        participants = [
            user for user in team.participants if user.id not in to_remove_ids
        ]

        if to_add_ids:
            participants_to_add = await self.session.execute(
                select(User).filter(User.id.in_(to_add_ids))
            )
            participants_to_add = participants_to_add.scalars().all()
            participants += participants_to_add

        team.participants = participants
        self.session.add(team)
        await self.session.flush()
        return team.to_entity()

    async def fetch_all(self) -> Sequence[TeamEntity]:
        teams = await self._fetch_all(self.session)
        return [team.to_entity() for team in teams]

    async def fetch_by_id(self, id_: int) -> TeamEntity | None:
        team = await self._fetch_by_id(self.session, id_)
        return team.to_entity() if team else None
