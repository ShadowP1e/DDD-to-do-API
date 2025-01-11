from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import HTTPBearer

from features.task.presentation.v1.endpoints.assign_task import assign_task
from features.task.presentation.v1.endpoints.create_task import create_task
from features.task.presentation.v1.endpoints.delete_task import delete_task
from features.task.presentation.v1.endpoints.get_task import get_task
from features.task.presentation.v1.endpoints.get_team_tasks import get_team_tasks
from features.task.presentation.v1.endpoints.unassign_task import unassign_task
from features.task.presentation.v1.schemas import TaskResponse

http_bearer = HTTPBearer(auto_error=False)  # Only for openapi.json

router = APIRouter(prefix='/api/v1', tags=['tasks'])

router.add_api_route(
    '/teams/{team_id}/tasks',
    create_task,
    methods=['POST'],
    dependencies=[Depends(http_bearer)],
    status_code=201,
    responses={
        201: {"description": "Task created successfully", "model": TaskResponse},
        400: {"description": "Bad request. Invalid input data."},
        401: {"description": "Unauthorized. Invalid credentials."},
        403: {"description": "Forbidden. You are not a participant of the team."},
        404: {"description": "Not found. Team does not exist."}
    }
)

router.add_api_route(
    '/teams/{team_id}/tasks',
    get_team_tasks,
    methods=['GET'],
    dependencies=[Depends(http_bearer)],
    status_code=200,
    responses={
        200: {"description": "Tasks retrieved successfully", "model": list[TaskResponse]},
        401: {"description": "Unauthorized. Invalid credentials."},
        403: {"description": "Forbidden. You are not a participant of the team."}
    }
)

router.add_api_route(
    '/tasks/{task_id}',
    get_task,
    methods=['GET'],
    dependencies=[Depends(http_bearer)],
    status_code=200,
    responses={
        200: {"description": "Task details retrieved successfully", "model": TaskResponse},
        401: {"description": "Unauthorized. Invalid credentials."},
        403: {"description": "Forbidden. You are not a participant of the team."},
        404: {"description": "Not found. Task does not exist."}
    }
)

router.add_api_route(
    '/tasks/{task_id}',
    delete_task,
    methods=['DELETE'],
    dependencies=[Depends(http_bearer)],
    status_code=200,
    responses={
        200: {"description": "Task deleted successfully", "model": TaskResponse},
        401: {"description": "Unauthorized. Invalid credentials."},
        403: {"description": "Forbidden. You are not a participant of the team."},
        404: {"description": "Not found. Task does not exist."}
    }
)

router.add_api_route(
    '/tasks/{task_id}/assign/{assignee_id}',
    assign_task,
    methods=['PUT'],
    dependencies=[Depends(http_bearer)],
    status_code=200,
    responses={
        200: {"description": "Task assigned successfully", "model": TaskResponse},
        400: {"description": "Bad request. Invalid task or assignee."},
        401: {"description": "Unauthorized. Invalid credentials."},
        403: {"description": "Forbidden. You are not a participant of the team."},
        404: {"description": "Not found. Task or assignee does not exist."}
    }
)

router.add_api_route(
    '/tasks/{task_id}/assign',
    unassign_task,
    methods=['DELETE'],
    dependencies=[Depends(http_bearer)],
    status_code=200,
    responses={
        200: {"description": "Task unassigned successfully", "model": TaskResponse},
        401: {"description": "Unauthorized. Invalid credentials."},
        403: {"description": "Forbidden. You are not a participant of the team."},
        404: {"description": "Not found. Task does not exist."}
    }
)
