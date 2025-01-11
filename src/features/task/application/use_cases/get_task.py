from typing import Sequence

from core.event_dispatcher import EventDispatcher
from core.interfaces.use_case import BaseUseCase
from features.task.domain.actions.queries import GetTaskQuery
from features.task.domain.entities.task_query_model import TaskReadModel
from features.task.domain.exceptions import TaskDoesNotExistError
from features.task.domain.services.task_query_service import TaskQueryService
from features.team.domain.actions.queries import GetTeamQuery
from features.team.domain.exceptions import NotTeamParticipantError


class GetTaskUseCase(BaseUseCase[GetTaskQuery, TaskReadModel]):
    def __init__(self, service: TaskQueryService, event_dispatcher: EventDispatcher):
        self.service = service
        self.event_dispatcher = event_dispatcher

    async def execute(self, data: GetTaskQuery) -> TaskReadModel:
        task = await self.service.fetch_by_id(data.task_id)

        if task is None:
            raise TaskDoesNotExistError("Task does not exist")

        if all(participant.id != data.current_user_id for participant in task.team.participants):
            raise NotTeamParticipantError("User is not a participant of the team.")

        return task
