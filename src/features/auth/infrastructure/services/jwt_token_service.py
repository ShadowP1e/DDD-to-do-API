from datetime import UTC, datetime, timedelta
from typing import Any

from jose import ExpiredSignatureError, JWTError, jwt

from features.auth.domain.exceptions import AuthorizationError
from features.auth.domain.services.token_service import TokenService


class JWTTokenService(TokenService):
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(self, payload: dict[str, Any], expires_in: int) -> str:
        issued_at = datetime.now(tz=UTC)
        expiration = issued_at + timedelta(seconds=expires_in)
        payload["exp"] = int(expiration.timestamp())
        payload["iat"] = int(issued_at.timestamp())
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

        except ExpiredSignatureError as e:
            raise AuthorizationError("Token has expired") from e

        except JWTError as e:
            raise AuthorizationError("Invalid token") from e

        except AttributeError as e:
            raise AuthorizationError("Invalid token") from e
