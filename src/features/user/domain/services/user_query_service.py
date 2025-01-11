from abc import ABC, abstractmethod

from core.interfaces.query_service import BaseQueryService
from features.user.domain.entities.user_query_model import UserReadModel


class UserQueryService(BaseQueryService[UserReadModel], ABC):
    @abstractmethod
    async def fetch_by_email(self, email: str) -> UserReadModel | None:
        raise NotImplementedError()
