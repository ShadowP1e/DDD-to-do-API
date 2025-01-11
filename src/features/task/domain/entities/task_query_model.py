from dataclasses import dataclass
from datetime import datetime

from features.task.domain.entities.task_entity import TaskEntity
from features.team.domain.entities.team_query_model import TeamReadModel
from features.user.domain.entities.user_query_model import UserReadModel


@dataclass
class TaskReadModel:
    id: int
    title: str
    description: str
    team_id: int
    creator_id: int
    assignee_id: int | None = None
    deadline: datetime | None = None

    team: TeamReadModel | None = None
    creator: UserReadModel | None = None
    assignee: UserReadModel | None = None

    @classmethod
    def from_entity(cls, entity: TaskEntity) -> 'TaskReadModel':
        # TODO: FIX CODE DUPLICATE
        return cls(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            team_id=entity.team_id,
            creator_id=entity.creator_id,
            assignee_id=entity.assignee_id,
            deadline=entity.deadline,
            team=TeamReadModel.from_entity(entity.team) if entity.team else None,
            creator=UserReadModel.from_entity(entity.creator) if entity.creator else None,
            assignee=UserReadModel.from_entity(entity.assignee) if entity.assignee else None,
        )
