from abc import ABC, abstractmethod

from core.interfaces.unit_of_work import BaseUnitOfWork
from features.team.domain.repositories.team_repository import TeamRepository
from features.user.domain.repositories.user_repository import UserRepository
from features.task.domain.repositories.task_repository import TaskRepository


class TaskUnitOfWork(BaseUnitOfWork, ABC):
    @property
    @abstractmethod
    def user_repository(self) -> UserRepository:
        ...

    @property
    @abstractmethod
    def task_repository(self) -> TaskRepository:
        ...

    @property
    @abstractmethod
    def team_repository(self) -> TeamRepository:
        ...