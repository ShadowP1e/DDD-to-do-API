from typing import Sequence

from core.event_dispatcher import EventDispatcher
from core.interfaces.use_case import BaseUseCase
from features.team.domain.actions.queries import GetTeamsWithUserQuery
from features.team.domain.entities.team_query_model import TeamReadModel
from features.team.domain.services.team_query_service import TeamQueryService


class GetTeamsWithUserUseCase(BaseUseCase[GetTeamsWithUserQuery, TeamReadModel]):
    def __init__(self, service: TeamQueryService, event_dispatcher: EventDispatcher):
        self.service = service
        self.event_dispatcher = event_dispatcher

    async def execute(self, data: GetTeamsWithUserQuery) -> Sequence[TeamReadModel]:
        teams = await self.service.fetch_all_with_user(data.user_id)

        return teams
