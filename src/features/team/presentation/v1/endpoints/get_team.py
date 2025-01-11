from typing import Awaitable, Callable

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request

from container import Container
from features.auth.domain.exceptions import AuthorizationError
from features.team.application.use_cases.get_team import GetTeamUseCase
from features.team.domain.actions.queries import GetTeamQuery
from features.team.domain.exceptions import NotTeamParticipantError, TeamDoesNotExistError
from features.team.presentation.v1.schemas import TeamResponse


@inject
async def get_team(
        team_id: int,
        request: Request,
        get_current_user_id: Callable[[Request], Awaitable[int]] = Depends(Provide[Container.current_user_provider]),
        get_team_use_case: GetTeamUseCase = Depends(Provide[Container.get_team_use_case])
) -> TeamResponse:
    try:
        current_user_id = await get_current_user_id(request)

        command = GetTeamQuery(id=team_id, user_id=current_user_id)
        team = await get_team_use_case.execute(command)

        return TeamResponse.model_validate(team, from_attributes=True)

    except AuthorizationError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e

    except NotTeamParticipantError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e

    except TeamDoesNotExistError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
