from dataclasses import dataclass

from core.actions.base import BaseAction


@dataclass
class CreateUserCommand(BaseAction):
    email: str
    password: str


@dataclass
class UpdateUserCommand(BaseAction):
    email: str | None = None
    password: str | None = None
