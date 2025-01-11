from typing import Awaitable, Callable

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request

from container import Container
from features.auth.domain.exceptions import AuthorizationError
from features.team.application.use_cases.add_team_participant import AddTeamParticipantUseCase
from features.team.domain.actions.commands import AddParticipantTeamCommand
from features.team.domain.exceptions import NotTeamOwnerError
from features.team.presentation.v1.schemas import TeamResponse


@inject
async def add_team_participant(
        team_id: int,
        user_id: int,
        request: Request,
        add_team_participant_use_case: AddTeamParticipantUseCase = Depends(
            Provide[Container.add_team_participant_use_case]
        ),
        get_current_user_id: Callable[[Request], Awaitable[int]] = Depends(Provide[Container.current_user_provider]),
) -> TeamResponse:
    try:
        current_user_id = await get_current_user_id(request)
        command = AddParticipantTeamCommand(user_id=user_id, team_id=team_id, current_user_id=current_user_id)
        team = await add_team_participant_use_case.execute(command)
        return TeamResponse.model_validate(team, from_attributes=True)

    except AuthorizationError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e

    except NotTeamOwnerError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e
