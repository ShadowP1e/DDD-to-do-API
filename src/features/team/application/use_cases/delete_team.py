from core.event_dispatcher import EventDispatcher
from core.interfaces.use_case import BaseUseCase
from features.team.domain.actions.commands import DeleteTeamCommand
from features.team.domain.entities.team_query_model import TeamReadModel
from features.team.domain.exceptions import NotTeamOwnerError, TeamDoesNotExistError
from features.team.domain.repositories.team_unit_of_work import TeamUnitOfWork


class DeleteTeamUseCase(BaseUseCase[DeleteTeamCommand, TeamReadModel]):
    def __init__(self, uow: TeamUnitOfWork, event_dispatcher: EventDispatcher):
        self.uow = uow
        self.event_dispatcher = event_dispatcher

    async def execute(self, data: DeleteTeamCommand) -> TeamReadModel:
        async with self.uow as uow:
            team = await uow.team_repository.fetch_by_id(data.team_id)

            if team is None:
                raise TeamDoesNotExistError("Team does not exist")

            if team.owner_id != data.current_user_id:
                raise NotTeamOwnerError("Not a team owner")

            await uow.team_repository.delete_by_id(team.id)
            await uow.commit()

            await self.event_dispatcher.dispatch(team.get_events())

            return TeamReadModel.from_entity(team)
