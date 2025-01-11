from abc import ABC, abstractmethod

from core.interfaces.repository import BaseRepository
from features.user.domain.entities.user_entity import UserEntity


class UserRepository(BaseRepository[UserEntity], ABC):
    @abstractmethod
    async def fetch_by_email(self, email: str) -> UserEntity | None:
        raise NotImplementedError()
