from typing import Sequence

from core.event_dispatcher import EventDispatcher
from core.interfaces.use_case import BaseUseCase
from features.task.domain.actions.queries import GetTeamTasksQuery
from features.task.domain.entities.task_query_model import TaskReadModel
from features.task.domain.services.task_query_service import TaskQueryService
from features.team.domain.exceptions import NotTeamParticipantError


class GetTeamTasksUseCase(BaseUseCase[GetTeamTasksQuery, TaskReadModel]):
    def __init__(self, service: TaskQueryService, event_dispatcher: EventDispatcher):
        self.service = service
        self.event_dispatcher = event_dispatcher

    async def execute(self, data: GetTeamTasksQuery) -> Sequence[TaskReadModel]:
        participants = await self.service.fetch_team_participants(data.team_id)

        if all(participant.id != data.current_user_id for participant in participants):
            raise NotTeamParticipantError("User is not a participant of the team.")

        tasks = await self.service.fetch_all_by_team(data.team_id)

        return tasks
