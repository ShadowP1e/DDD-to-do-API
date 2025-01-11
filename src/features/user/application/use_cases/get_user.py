from core.event_dispatcher import EventDispatcher
from core.interfaces.use_case import BaseUseCase
from features.user.domain.actions.queries import GetUserQuery
from features.user.domain.entities.user_entity import UserEntity
from features.user.domain.entities.user_query_model import UserReadModel
from features.user.domain.exceptions import UserDoesNotExistError
from features.user.domain.services.user_query_service import UserQueryService


class GetUserUseCase(BaseUseCase[UserEntity, UserReadModel]):
    def __init__(self, service: UserQueryService, event_dispatcher: EventDispatcher):
        self.service = service
        self.event_dispatcher = event_dispatcher

    async def execute(self, data: GetUserQuery) -> UserReadModel:
        user = await self.service.fetch_by_id(data.id)
        if not user:
            raise UserDoesNotExistError("User does not exist")

        return user
