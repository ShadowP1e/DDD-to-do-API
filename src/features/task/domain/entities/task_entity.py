import copy
from datetime import datetime

from core.entities.base import BaseDomainEntity
from features.user.domain.entities.user_entity import UserEntity
from features.team.domain.entities.team_entity import TeamEntity
from features.task.domain.actions.commands import CreateTaskCommand, UpdateTaskCommand
from features.task.domain.events.task_created import TaskCreatedEvent
from features.task.domain.events.task_updated import TaskUpdatedEvent


class TaskEntity(BaseDomainEntity):
    def __init__(
            self,
            id_: int | None,
            title: str,
            description: str,
            team_id: int,
            creator_id: int,
            assignee_id: int | None = None,
            deadline: datetime | None = None,

            team: TeamEntity | None = None,
            creator: UserEntity | None = None,
            assignee: UserEntity | None = None,
    ):
        super().__init__(id_=id_)
        self.title = title
        self.description = description
        self.team_id = team_id
        self.team = team
        self.creator_id = creator_id
        self.creator = creator
        self.assignee_id = assignee_id
        self.assignee = assignee
        self.deadline = deadline

    def assign_user(self, user: 'UserEntity'):
        self.assignee = user
        self.assignee_id = user.id

    def unassign_user(self):
        self.assignee = None
        self.assignee_id = None

    @classmethod
    def create(cls, entity_create_model: 'CreateTaskCommand') -> 'TaskEntity':
        task = cls(
            id_=None,
            **entity_create_model.to_dict()
        )
        task.add_event(TaskCreatedEvent(task.id, task.title, task.creator_id, task.team_id))
        return task

    def update(self, entity_update_model: 'UpdateTaskCommand') -> 'TaskEntity':
        update_data = entity_update_model.to_dict()
        updated_task = copy.deepcopy(self)

        for attr_name, value in update_data.items():
            setattr(updated_task, attr_name, value)

        updated_task.add_event(TaskUpdatedEvent(self.id, self.title, self.creator_id, self.team_id))
        return updated_task

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TaskEntity):
            return self.id == other.id
        return False
