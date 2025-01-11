from core.event_dispatcher import EventDispatcher
from core.interfaces.use_case import BaseUseCase
from features.task.domain.actions.commands import UnassignTaskCommand
from features.task.domain.entities.task_query_model import TaskReadModel
from features.task.domain.repositories.task_unit_of_work import TaskUnitOfWork
from features.team.domain.exceptions import NotTeamParticipantError


class UnassignTaskUseCase(BaseUseCase[UnassignTaskCommand, TaskReadModel]):
    def __init__(self, uow: TaskUnitOfWork, event_dispatcher: EventDispatcher):
        self.uow = uow
        self.event_dispatcher = event_dispatcher

    async def execute(self, data: UnassignTaskCommand) -> TaskReadModel:
        async with self.uow as uow:
            task = await uow.task_repository.fetch_by_id(data.task_id)
            if not task:
                raise ValueError(f"Task with ID {data.task_id} does not exist.")

            if all(user.id != data.current_user_id for user in task.team.participants):
                raise NotTeamParticipantError("Not team participant")

            task.unassign_user()

            await uow.task_repository.update(task)
            await uow.commit()

            await self.event_dispatcher.dispatch(task.get_events())

            return TaskReadModel.from_entity(task)
