from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.models.postgres.models import Base
from features.user.domain.entities.user_entity import UserEntity
from features.user.domain.entities.user_query_model import UserReadModel


class User(Base):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)

    def to_entity(self) -> 'UserEntity':
        return UserEntity(
            id_=self.id,
            email=self.email,
            password=self.password,
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
        }

    def to_read_model(self) -> 'UserReadModel':
        return UserReadModel(
            id=self.id,
            email=self.email,
            password=self.password,
        )

    @classmethod
    def from_entity(cls, user: 'UserEntity') -> 'User':
        return cls(
            id=user.id,
            email=user.email,
            password=user.password,
        )
