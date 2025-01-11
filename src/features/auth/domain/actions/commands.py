from dataclasses import dataclass

from core.actions.base import BaseAction


@dataclass
class UserLoginCommand(BaseAction):
    email: str
    password: str


@dataclass
class RefreshTokenCommand(BaseAction):
    refresh_token: str
