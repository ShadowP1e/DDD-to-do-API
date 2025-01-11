from dataclasses import dataclass

from core.interfaces.domain_event import BaseDomainEvent
from features.team.domain.events.team_events import TeamEvents


@dataclass
class TeamUpdatedEvent(BaseDomainEvent):
    id: int
    name: str
    owner_id: int

    @staticmethod
    def get_event_name() -> str:
        return TeamEvents.UPDATED.value
