from abc import ABC

from core.interfaces.repository import BaseRepository
from features.task.domain.entities.task_entity import TaskEntity


class TaskRepository(BaseRepository[TaskEntity], ABC):
    ...
