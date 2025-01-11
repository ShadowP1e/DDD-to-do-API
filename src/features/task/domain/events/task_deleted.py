from dataclasses import dataclass

from core.interfaces.domain_event import BaseDomainEvent
from features.task.domain.events.task_events import TaskEvents


@dataclass
class TaskDeletedEvent(BaseDomainEvent):
    id: int
    title: str
    creator_id: int
    team_id: int

    @staticmethod
    def get_event_name() -> str:
        return TaskEvents.DELETED.value
