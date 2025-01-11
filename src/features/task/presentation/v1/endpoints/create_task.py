from typing import Awaitable, Callable

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request

from container import Container
from features.auth.domain.exceptions import AuthorizationError
from features.task.application.use_cases.create_task import CreateTaskUseCase
from features.task.domain.actions.commands import CreateTaskCommand
from features.task.presentation.v1.schemas import CreateTaskRequest, TaskResponse
from features.team.application.use_cases.create_team import CreateTeamUseCase
from features.team.domain.actions.commands import CreateTeamCommand
from features.team.domain.exceptions import NotTeamParticipantError, TeamDoesNotExistError
from features.team.presentation.v1.schemas import CreateTeamRequest, TeamResponse


@inject
async def create_task(
        team_id: int,
        request: Request,
        schema: CreateTaskRequest,
        create_task_use_case: CreateTaskUseCase = Depends(Provide[Container.create_task_use_case]),
        get_current_user_id: Callable[[Request], Awaitable[int]] = Depends(Provide[Container.current_user_provider]),
) -> TaskResponse:
    try:
        current_user_id = await get_current_user_id(request)
        command = CreateTaskCommand(
            title=schema.title,
            description=schema.description,
            team_id=team_id,
            creator_id=current_user_id,
            deadline=schema.deadline,
        )
        task = await create_task_use_case.execute(command)
        return TaskResponse.model_validate(task, from_attributes=True)

    except AuthorizationError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e

    except TeamDoesNotExistError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    except NotTeamParticipantError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e
