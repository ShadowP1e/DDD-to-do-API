from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException

from container import Container
from features.user.application.use_cases.create_user import CreateUserUseCase
from features.user.domain.actions.commands import CreateUserCommand
from features.user.domain.exceptions import UserAlreadyExistsError
from features.user.presentation.v1.schemas import CreateUserRequest, UserResponse


@inject
async def create_user(
        schema: CreateUserRequest,
        create_user_use_case: CreateUserUseCase = Depends(Provide[Container.create_user_use_case]),
) -> UserResponse:
    try:
        command = CreateUserCommand(email=schema.email, password=schema.password)
        user = await create_user_use_case.execute(command)
        return UserResponse(id=user.id, email=user.email)

    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
