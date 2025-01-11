from abc import ABC, abstractmethod

from core.interfaces.unit_of_work import BaseUnitOfWork
from features.user.domain.repositories.user_repository import UserRepository


class UserUnitOfWork(BaseUnitOfWork, ABC):
    @property
    @abstractmethod
    def user_repository(self) -> UserRepository:
        ...
