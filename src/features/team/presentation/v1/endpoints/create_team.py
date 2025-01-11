from typing import Awaitable, Callable

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request

from container import Container
from features.auth.domain.exceptions import AuthorizationError
from features.team.application.use_cases.create_team import CreateTeamUseCase
from features.team.domain.actions.commands import CreateTeamCommand
from features.team.presentation.v1.schemas import CreateTeamRequest, TeamResponse


@inject
async def create_team(
        request: Request,
        schema: CreateTeamRequest,
        create_team_use_case: CreateTeamUseCase = Depends(Provide[Container.create_team_use_case]),
        get_current_user_id: Callable[[Request], Awaitable[int]] = Depends(Provide[Container.current_user_provider]),
) -> TeamResponse:
    try:
        current_user_id = await get_current_user_id(request)
        command = CreateTeamCommand(name=schema.name, owner_id=current_user_id)
        team = await create_team_use_case.execute(command)
        return TeamResponse.model_validate(team, from_attributes=True)

    except AuthorizationError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e
