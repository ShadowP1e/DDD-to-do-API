import asyncio

from core.event_dispatcher import EventDispatcher
from core.interfaces.use_case import BaseUseCase
from features.task.domain.actions.commands import CreateTaskCommand
from features.task.domain.entities.task_entity import TaskEntity
from features.task.domain.entities.task_query_model import TaskReadModel
from features.task.domain.repositories.task_unit_of_work import TaskUnitOfWork
from features.team.domain.exceptions import NotTeamParticipantError, TeamDoesNotExistError


class CreateTaskUseCase(BaseUseCase[CreateTaskCommand, TaskReadModel]):
    def __init__(self, uow: TaskUnitOfWork, event_dispatcher: EventDispatcher):
        self.uow = uow
        self.event_dispatcher = event_dispatcher

    async def execute(self, data: CreateTaskCommand) -> TaskReadModel:
        async with self.uow as uow:
            team = await uow.team_repository.fetch_by_id(data.team_id)

            if team is None:
                raise TeamDoesNotExistError("Team does not exist")

            if all(user.id != data.creator_id for user in team.participants):
                raise NotTeamParticipantError("Not team participant")

            task = await asyncio.to_thread(TaskEntity.create, data)

            created_task = await uow.task_repository.create(task)
            await uow.commit()

            await self.event_dispatcher.dispatch(task.get_events())

            return TaskReadModel.from_entity(created_task)
