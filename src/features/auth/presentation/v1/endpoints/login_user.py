from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException

from container import Container
from features.auth.application.use_cases.login_user import LoginUserUseCase
from features.auth.domain.actions.commands import UserLoginCommand
from features.auth.domain.exceptions import InvalidCredentialsError
from features.auth.presentation.v1.schemas import LoginUserRequest, TokensResponse


@inject
async def login_user(
        schema: LoginUserRequest,
        login_user_use_case: LoginUserUseCase = Depends(Provide[Container.login_user_use_case]),
) -> TokensResponse:
    try:
        command = UserLoginCommand(email=schema.email, password=schema.password)
        tokens = await login_user_use_case.execute(command)
        return TokensResponse(tokens=tokens)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e
