import enum


class TaskEvents(enum.Enum):
    CREATED = "TaskCreatedEvent"
    UPDATED = "TaskUpdatedEvent"
    DELETED = "TaskDeletedEvent"
