import enum


class UserEvents(enum.Enum):
    CREATED = "UserCreatedEvent"
    UPDATED = "UserUpdatedEvent"
    DELETED = "UserDeletedEvent"
