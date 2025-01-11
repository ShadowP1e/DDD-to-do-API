import enum


class TeamEvents(enum.Enum):
    CREATED = "TeamCreatedEvent"
    UPDATED = "TeamUpdatedEvent"
    DELETED = "TeamDeletedEvent"
