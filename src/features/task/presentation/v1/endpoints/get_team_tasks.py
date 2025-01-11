from typing import Awaitable, Callable

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request

from container import Container
from features.auth.domain.exceptions import AuthorizationError
from features.task.application.use_cases.get_team_tasks import GetTeamTasksUseCase
from features.task.domain.actions.queries import GetTeamTasksQuery
from features.task.presentation.v1.schemas import TaskResponse
from features.team.domain.exceptions import NotTeamParticipantError


@inject
async def get_team_tasks(
        team_id: int,
        request: Request,
        get_current_user_id: Callable[[Request], Awaitable[int]] = Depends(Provide[Container.current_user_provider]),
        get_team_tasks_use_case: GetTeamTasksUseCase = Depends(Provide[Container.get_team_tasks_use_case])
) -> list[TaskResponse]:
    try:
        current_user_id = await get_current_user_id(request)

        command = GetTeamTasksQuery(team_id=team_id, current_user_id=current_user_id)
        tasks = await get_team_tasks_use_case.execute(command)

        return [TaskResponse.model_validate(task, from_attributes=True) for task in tasks]

    except AuthorizationError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e

    except NotTeamParticipantError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e
