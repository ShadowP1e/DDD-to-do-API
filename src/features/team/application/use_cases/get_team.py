from core.event_dispatcher import EventDispatcher
from core.interfaces.use_case import BaseUseCase
from features.team.domain.actions.queries import GetTeamQuery
from features.team.domain.entities.team_entity import TeamEntity
from features.team.domain.entities.team_query_model import TeamReadModel
from features.team.domain.exceptions import NotTeamParticipantError, TeamDoesNotExistError
from features.team.domain.services.team_query_service import TeamQueryService


class GetTeamUseCase(BaseUseCase[GetTeamQuery, TeamReadModel]):
    def __init__(self, service: TeamQueryService, event_dispatcher: EventDispatcher):
        self.service = service
        self.event_dispatcher = event_dispatcher

    async def execute(self, data: GetTeamQuery) -> TeamReadModel:
        team = await self.service.fetch_by_id(data.id)
        if not team:
            raise TeamDoesNotExistError("Team does not exist")

        if all(user.id != data.user_id for user in team.participants):
            raise NotTeamParticipantError("Not team participant")

        return team
