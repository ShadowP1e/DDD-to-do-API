from typing import Any

from starlette.requests import Request

from features.auth.domain.exceptions import AuthorizationError
from features.auth.domain.services.token_service import TokenService
from features.auth.domain.strategies.auth_strategy import AuthStrategy
from features.auth.infrastructure.services.jwt_token_service import JWTTokenService


class JWTAuthStrategy(AuthStrategy):
    def __init__(self, jwt_secret_key: str, jwt_algorithm: str):
        self._jwt_secret_key = jwt_secret_key
        self._jwt_algorithm = jwt_algorithm
        self._token_service: TokenService | None = None

    @property
    def token_service(self) -> TokenService:
        if self._token_service is None:
            self._token_service = JWTTokenService(self._jwt_secret_key, self._jwt_algorithm)
        return self._token_service

    def login(self, user_id: int) -> dict[str, str]:
        access_token = self.token_service.create_token(
            {
                "sub": str(user_id),
                "type": "access",
            },
            expires_in=60 * 60
        )
        refresh_token = self.token_service.create_token(
            {
                "sub": str(user_id),
                "type": "refresh",
            },
            expires_in=60 * 60 * 24
        )
        return {"access_token": access_token, "refresh_token": refresh_token}

    def validate(self, token: str) -> dict[str, Any]:
        payload = self.token_service.decode_token(token)

        return payload

    def logout(self, user_id: int, token: str):
        pass

    def extract_token(self, request: Request) -> str:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise AuthorizationError("Invalid Authorization header")

        if not auth_header.startswith("Bearer "):
            raise AuthorizationError("Authorization header must start with Bearer")

        return auth_header.split(" ", 1)[1]
