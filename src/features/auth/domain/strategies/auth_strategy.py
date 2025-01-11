from abc import ABC, abstractmethod
from typing import Any

from fastapi import Request


class AuthStrategy(ABC):
    @abstractmethod
    def login(self, user_id: int) -> dict[str, str]:
        pass

    @abstractmethod
    def validate(self, token: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def logout(self, user_id: int, token: str):
        pass

    @abstractmethod
    def extract_token(self, request: Request) -> str:
        pass
