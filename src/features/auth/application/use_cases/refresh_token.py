from core.interfaces.use_case import BaseUseCase
from features.auth.domain.actions.commands import RefreshTokenCommand
from features.auth.domain.exceptions import AuthorizationError
from features.auth.domain.strategies.auth_strategy import AuthStrategy


class RefreshTokenUseCase(BaseUseCase[RefreshTokenCommand, dict[str, str]]):
    def __init__(self, auth_strategy: AuthStrategy):
        self.auth_strategy = auth_strategy

    async def execute(self, data: RefreshTokenCommand) -> dict[str, str]:
        payload = self.auth_strategy.validate(data.refresh_token)

        user_id = payload.get('sub')
        if user_id is None:
            raise AuthorizationError('Invalid token payload')

        user_id = int(user_id)

        tokens = self.auth_strategy.login(user_id=user_id)
        return tokens
