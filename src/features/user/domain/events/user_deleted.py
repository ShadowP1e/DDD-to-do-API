from pydantic.dataclasses import dataclass

from core.interfaces.domain_event import BaseDomainEvent
from features.user.domain.events.user_events import UserEvents


@dataclass
class UserDeletedEvent(BaseDomainEvent):
    id: int
    email: str

    @staticmethod
    def get_event_name() -> str:
        return UserEvents.DELETED.value