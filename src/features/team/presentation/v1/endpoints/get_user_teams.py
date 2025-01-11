from typing import Awaitable, Callable

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request

from container import Container
from features.auth.domain.exceptions import AuthorizationError
from features.team.application.use_cases.get_user_teams import GetTeamsWithUserUseCase
from features.team.domain.actions.queries import GetTeamsWithUserQuery
from features.team.presentation.v1.schemas import TeamResponse


@inject
async def get_user_teams(
        request: Request,
        get_current_user_id: Callable[[Request], Awaitable[int]] = Depends(Provide[Container.current_user_provider]),
        get_teams_with_user_use_case: GetTeamsWithUserUseCase = Depends(Provide[Container.get_teams_with_user_use_case])
) -> list[TeamResponse]:
    try:
        current_user_id = await get_current_user_id(request)

        command = GetTeamsWithUserQuery(user_id=current_user_id)
        teams = await get_teams_with_user_use_case.execute(command)

        return [TeamResponse.model_validate(team, from_attributes=True) for team in teams]

    except AuthorizationError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e
