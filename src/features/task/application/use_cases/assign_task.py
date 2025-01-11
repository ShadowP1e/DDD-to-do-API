from core.event_dispatcher import EventDispatcher
from core.interfaces.use_case import BaseUseCase
from features.task.domain.actions.commands import AssignTaskCommand
from features.task.domain.entities.task_query_model import TaskReadModel
from features.task.domain.exceptions import TaskDoesNotExistError
from features.task.domain.repositories.task_unit_of_work import TaskUnitOfWork
from features.team.domain.exceptions import NotTeamParticipantError


class AssignTaskUseCase(BaseUseCase[AssignTaskCommand, TaskReadModel]):
    def __init__(self, uow: TaskUnitOfWork, event_dispatcher: EventDispatcher):
        self.uow = uow
        self.event_dispatcher = event_dispatcher

    async def execute(self, data: AssignTaskCommand) -> TaskReadModel:
        async with self.uow as uow:
            task = await uow.task_repository.fetch_by_id(data.task_id)
            if not task:
                raise TaskDoesNotExistError(f"Task does not exist.")

            if all(user.id != data.current_user_id for user in task.team.participants):
                raise NotTeamParticipantError("Not team participant")

            if all(user.id != data.assignee_id for user in task.team.participants):
                raise NotTeamParticipantError("Not team participant")

            user = await uow.user_repository.fetch_by_id(data.assignee_id)

            task.assign_user(user)

            await uow.task_repository.update(task)
            await uow.commit()

            await self.event_dispatcher.dispatch(task.get_events())

            return TaskReadModel.from_entity(task)
