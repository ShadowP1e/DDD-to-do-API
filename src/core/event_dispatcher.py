import asyncio
from typing import Callable

from core.interfaces.domain_event import BaseDomainEvent


class EventDispatcher:
    def __init__(self, handlers: dict[str, list[Callable]] = None):
        self._handlers = handlers or {}

    def register_handler(self, event_name: str, handler: Callable):
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)

    async def dispatch(self, events: list[BaseDomainEvent]):
        tasks = []
        for event in events:
            handlers = self._handlers.get(event.get_event_name(), [])
            if not handlers:
                return

            for handler_provider in handlers:
                handler_instance = handler_provider()
                tasks.append(handler_instance.handle(event))

        await asyncio.gather(*tasks)
