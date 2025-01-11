from abc import ABC, abstractmethod
from typing import Any


class TokenService(ABC):
    @abstractmethod
    def create_token(self, payload: dict[str, Any], expires_in: int) -> str:
        pass

    @abstractmethod
    def decode_token(self, token: str) -> dict[str, Any]:
        pass
