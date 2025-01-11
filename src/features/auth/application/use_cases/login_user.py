from core.interfaces.use_case import BaseUseCase
from core.security.password_hashing import verify_password
from features.auth.domain.actions.commands import UserLoginCommand
from features.auth.domain.exceptions import InvalidCredentialsError
from features.auth.domain.strategies.auth_strategy import AuthStrategy
from features.user.domain.services.user_query_service import UserQueryService


class LoginUserUseCase(BaseUseCase[UserLoginCommand, dict[str, str]]):
    def __init__(self, auth_strategy: AuthStrategy, user_query_service: UserQueryService):
        self.auth_strategy = auth_strategy
        self.user_query_service = user_query_service

    async def execute(self, data: UserLoginCommand) -> dict[str, str]:
        user = await self.user_query_service.fetch_by_email(data.email)

        if not user:
            raise InvalidCredentialsError("Invalid credentials")

        if not verify_password(data.password, user.password):
            raise InvalidCredentialsError("Invalid credentials")

        tokens = self.auth_strategy.login(user_id=user.id)
        return tokens
