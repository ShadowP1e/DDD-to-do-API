import asyncio

from core.event_dispatcher import EventDispatcher
from core.interfaces.use_case import BaseUseCase
from features.user.domain.actions.commands import CreateUserCommand
from features.user.domain.entities.user_entity import UserEntity
from features.user.domain.entities.user_query_model import UserReadModel
from features.user.domain.exceptions import UserAlreadyExistsError
from features.user.domain.repositories.user_unit_of_work import UserUnitOfWork


class CreateUserUseCase(BaseUseCase[CreateUserCommand, UserReadModel]):
    def __init__(self, uow: UserUnitOfWork, event_dispatcher: EventDispatcher):
        self.uow = uow
        self.event_dispatcher = event_dispatcher

    async def execute(self, data: CreateUserCommand) -> UserReadModel:
        async with self.uow as uow:
            if await (uow.user_repository.fetch_by_email(data.email)) is not None:
                raise UserAlreadyExistsError('User with this email already exists')

            # Creates a UserEntity object from the command in a separate thread to avoid blocking the main thread.
            user = await asyncio.to_thread(UserEntity.create, data)

            created_user = await uow.user_repository.create(user)
            await uow.commit()

            await self.event_dispatcher.dispatch(user.get_events())

            return UserReadModel.from_entity(created_user)
