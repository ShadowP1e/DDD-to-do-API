from typing import Awaitable, Callable

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request

from container import Container
from features.auth.domain.exceptions import AuthorizationError
from features.team.application.use_cases.remove_team_participant import RemoveTeamParticipantUseCase
from features.team.domain.actions.commands import RemoveParticipantTeamCommand
from features.team.domain.exceptions import CanNotRemoveOwnerError, NotTeamOwnerError
from features.team.presentation.v1.schemas import TeamResponse


@inject
async def remove_team_participant(
        team_id: int,
        user_id: int,
        request: Request,
        remove_team_participant_use_case: RemoveTeamParticipantUseCase = Depends(
            Provide[Container.remove_team_participant_use_case]
        ),
        get_current_user_id: Callable[[Request], Awaitable[int]] = Depends(Provide[Container.current_user_provider]),
) -> TeamResponse:
    try:
        current_user_id = await get_current_user_id(request)
        command = RemoveParticipantTeamCommand(user_id=user_id, team_id=team_id, current_user_id=current_user_id)
        team = await remove_team_participant_use_case.execute(command)
        return TeamResponse.model_validate(team, from_attributes=True)

    except AuthorizationError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e

    except CanNotRemoveOwnerError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    except NotTeamOwnerError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e
