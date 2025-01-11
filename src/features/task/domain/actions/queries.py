from dataclasses import dataclass

from core.actions.base import BaseAction


@dataclass
class GetTeamTasksQuery(BaseAction):
    team_id: int
    current_user_id: int


@dataclass
class GetTaskQuery(BaseAction):
    task_id: int
    current_user_id: int
