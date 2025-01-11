import asyncio

from core.event_dispatcher import EventDispatcher
from core.interfaces.use_case import BaseUseCase
from features.team.domain.actions.commands import CreateTeamCommand
from features.team.domain.entities.team_entity import TeamEntity
from features.team.domain.entities.team_query_model import TeamReadModel
from features.team.domain.repositories.team_unit_of_work import TeamUnitOfWork


class CreateTeamUseCase(BaseUseCase[CreateTeamCommand, TeamReadModel]):
    def __init__(self, uow: TeamUnitOfWork, event_dispatcher: EventDispatcher):
        self.uow = uow
        self.event_dispatcher = event_dispatcher

    async def execute(self, data: CreateTeamCommand) -> TeamReadModel:
        async with self.uow as uow:
            team = await asyncio.to_thread(TeamEntity.create, data)

            created_team = await uow.team_repository.create(team)
            await uow.commit()

            await self.event_dispatcher.dispatch(team.get_events())

            return TeamReadModel.from_entity(created_team)
