from fastapi import Request

from features.auth.domain.exceptions import AuthorizationError
from features.auth.domain.strategies.auth_strategy import AuthStrategy


class CurrentUserProvider:
    def __init__(self, auth_strategy: AuthStrategy):
        self.auth_strategy = auth_strategy

    async def __call__(self, request: Request, *args, **kwargs) -> int:
        token = self.auth_strategy.extract_token(request)
        payload = self.auth_strategy.validate(token)

        token_type = payload.get('type')
        if not token_type or token_type != 'access':
            raise AuthorizationError('Invalid token')

        user_id = payload.get("sub")
        if not user_id:
            raise AuthorizationError("Invalid token payload")

        return int(user_id)
