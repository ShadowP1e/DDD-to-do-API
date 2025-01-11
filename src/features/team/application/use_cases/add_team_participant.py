from core.event_dispatcher import EventDispatcher
from core.interfaces.use_case import BaseUseCase
from features.team.domain.actions.commands import AddParticipantTeamCommand
from features.team.domain.entities.team_query_model import TeamReadModel
from features.team.domain.exceptions import NotTeamOwnerError
from features.team.domain.repositories.team_unit_of_work import TeamUnitOfWork


class AddTeamParticipantUseCase(BaseUseCase[AddParticipantTeamCommand, TeamReadModel]):
    def __init__(self, uow: TeamUnitOfWork, event_dispatcher: EventDispatcher):
        self.uow = uow
        self.event_dispatcher = event_dispatcher

    async def execute(self, data: AddParticipantTeamCommand) -> TeamReadModel:
        async with self.uow as uow:
            team = await uow.team_repository.fetch_by_id(data.team_id)

            if team.owner_id != data.current_user_id:
                raise NotTeamOwnerError("Not team owner")

            participant = await uow.user_repository.fetch_by_id(data.user_id)

            team.add_participant(participant)

            team = await uow.team_repository.update(team)
            await uow.commit()

            await self.event_dispatcher.dispatch(team.get_events())

            return TeamReadModel.from_entity(team)
