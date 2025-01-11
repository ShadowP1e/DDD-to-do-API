from dataclasses import dataclass
from datetime import datetime

from core.actions.base import BaseAction


@dataclass
class CreateTaskCommand(BaseAction):
    title: str
    description: str
    team_id: int
    creator_id: int
    assignee_id: int | None = None
    deadline: datetime | None = None


@dataclass
class UpdateTaskCommand(BaseAction):
    task_id: int
    title: str | None = None
    description: str | None = None
    assignee_id: int | None = None
    deadline: datetime | None = None


@dataclass
class AssignTaskCommand(BaseAction):
    task_id: int
    assignee_id: int
    current_user_id: int


@dataclass
class UnassignTaskCommand(BaseAction):
    task_id: int
    current_user_id: int


@dataclass
class DeleteTaskCommand(BaseAction):
    task_id: int
    current_user_id: int
