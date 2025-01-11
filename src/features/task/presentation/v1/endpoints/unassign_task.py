from typing import Awaitable, Callable

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request

from container import Container
from features.auth.domain.exceptions import AuthorizationError
from features.task.application.use_cases.unassign_task import UnassignTaskUseCase
from features.task.domain.actions.commands import UnassignTaskCommand
from features.task.domain.exceptions import TaskDoesNotExistError
from features.task.presentation.v1.schemas import TaskResponse
from features.team.domain.exceptions import NotTeamParticipantError


@inject
async def unassign_task(
        task_id: int,
        request: Request,
        get_current_user_id: Callable[[Request], Awaitable[int]] = Depends(Provide[Container.current_user_provider]),
        unassign_task_use_case: UnassignTaskUseCase = Depends(Provide[Container.unassign_task_use_case])
) -> TaskResponse:
    try:
        current_user_id = await get_current_user_id(request)

        command = UnassignTaskCommand(
            task_id=task_id,
            current_user_id=current_user_id
        )
        task = await unassign_task_use_case.execute(command)

        return TaskResponse.model_validate(task, from_attributes=True)

    except AuthorizationError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e

    except TaskDoesNotExistError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    except NotTeamParticipantError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e
