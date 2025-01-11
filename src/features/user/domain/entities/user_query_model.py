from dataclasses import dataclass

from features.user.domain.entities.user_entity import UserEntity


@dataclass
class UserReadModel:
    id: int
    email: str
    password: str

    @classmethod
    def from_entity(cls, entity: UserEntity) -> 'UserReadModel':
        return cls(
            id=entity.id,
            email=entity.email,
            password=entity.password,
        )
