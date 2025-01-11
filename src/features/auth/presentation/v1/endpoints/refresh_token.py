from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException

from container import Container
from features.auth.application.use_cases.refresh_token import RefreshTokenUseCase
from features.auth.domain.actions.commands import RefreshTokenCommand
from features.auth.domain.exceptions import AuthorizationError
from features.auth.presentation.v1.schemas import RefreshTokenRequest, TokensResponse


@inject
async def refresh_token(
        schema: RefreshTokenRequest,
        refresh_token_use_case: RefreshTokenUseCase = Depends(Provide[Container.refresh_token_use_case]),
) -> TokensResponse:
    try:
        command = RefreshTokenCommand(refresh_token=schema.refresh_token)
        tokens = await refresh_token_use_case.execute(command)
        return TokensResponse(tokens=tokens)
    except AuthorizationError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e
