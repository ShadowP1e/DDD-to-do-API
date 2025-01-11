import copy

from core.entities.base import BaseDomainEntity
from core.security.password_hashing import get_password_hash, verify_password
from features.user.domain.actions.commands import CreateUserCommand, UpdateUserCommand
from features.user.domain.events.user_created import UserCreatedEvent
from features.user.domain.events.user_updated import UserUpdatedEvent


class UserEntity(BaseDomainEntity):
    def __init__(
            self,
            id_: int | None,
            email: str,
            password: str,
    ):
        super().__init__(id_=id_)
        self.email = email
        self._password = password

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str):
        self._password = get_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.password)

    @classmethod
    def create(cls, entity_create_model: 'CreateUserCommand') -> 'UserEntity':
        user = cls(
            id_=None,
            **entity_create_model.to_dict()
        )

        user.password = entity_create_model.password

        user.add_event(UserCreatedEvent(user.id, user.email))

        return user

    def update(self, entity_update_model: 'UpdateUserCommand') -> 'UserEntity':
        update_data = entity_update_model.to_dict()
        update_entity = copy.deepcopy(self)

        for attr_name, value in update_data.items():
            setattr(update_entity, attr_name, value)

        update_entity.add_event(UserUpdatedEvent(self.id, self.email))

        return update_entity

    def __eq__(self, other: object) -> bool:
        if isinstance(other, UserEntity):
            return self.id == other.id

        return False
