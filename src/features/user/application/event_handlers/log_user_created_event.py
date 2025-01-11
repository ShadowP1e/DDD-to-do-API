from features.user.domain.events.user_created import UserCreatedEvent
from features.user.infrastructure.services.logging_service import LoggingService


class LogUserCreatedEventHandler:
    def __init__(self, logging_service: LoggingService):
        self.logging_service = logging_service

    async def handle(self, event: UserCreatedEvent):
        await self.logging_service.log_event(
            message=f"User created with ID {event.id_} and email {event.email}"
        )
