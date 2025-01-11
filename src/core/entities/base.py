from core.interfaces.domain_event import BaseDomainEvent


class BaseDomainEntity:
    def __init__(self, id_: int | None):
        self.id = id_
        self._events: list[BaseDomainEvent] = []

    def add_event(self, event: BaseDomainEvent):
        self._events.append(event)

    def get_events(self) -> list[BaseDomainEvent]:
        events = self._events[:]
        self._events.clear()
        return events
