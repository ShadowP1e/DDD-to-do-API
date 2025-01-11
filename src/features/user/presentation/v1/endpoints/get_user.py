from typing import Awaitable, Callable

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request

from container import Container
from features.auth.domain.exceptions import AuthorizationError
from features.user.application.use_cases.get_user import GetUserUseCase
from features.user.domain.actions.queries import GetUserQuery
from features.user.domain.exceptions import UserDoesNotExistError
from features.user.presentation.v1.schemas import UserResponse


@inject
async def get_current_user(
        request: Request,
        get_current_user_id: Callable[[Request], Awaitable[int]] = Depends(Provide[Container.current_user_provider]),
        get_user_use_case: GetUserUseCase = Depends(Provide[Container.get_user_use_case])
) -> UserResponse:
    try:
        current_user_id = await get_current_user_id(request)

        command = GetUserQuery(id=current_user_id)
        user = await get_user_use_case.execute(command)

        return UserResponse(id=user.id, email=user.email)

    except UserDoesNotExistError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    except AuthorizationError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e
