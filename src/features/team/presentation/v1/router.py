from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from features.team.presentation.v1.endpoints.add_team_participant import add_team_participant
from features.team.presentation.v1.endpoints.create_team import create_team
from features.team.presentation.v1.endpoints.delete_team import delete_team
from features.team.presentation.v1.endpoints.get_team import get_team
from features.team.presentation.v1.endpoints.get_user_teams import get_user_teams
from features.team.presentation.v1.endpoints.remove_team_participant import remove_team_participant
from features.team.presentation.v1.schemas import TeamResponse

router = APIRouter(prefix='/api/v1', tags=['teams'])

http_bearer = HTTPBearer(auto_error=False)  # Only for openapi.json

router.add_api_route(
    '/teams',
    get_user_teams,
    methods=['GET'],
    dependencies=[Depends(http_bearer)],
    status_code=200,
    responses={
        200: {"description": "Retrieved teams for the current user", "model": list[TeamResponse]},
        401: {"description": "Unauthorized. User not authenticated."}
    }
)

router.add_api_route(
    '/teams/{team_id}',
    get_team,
    methods=['GET'],
    dependencies=[Depends(http_bearer)],
    status_code=200,
    responses={
        200: {"description": "Retrieved the team details", "model": TeamResponse},
        401: {"description": "Unauthorized. User not authenticated."},
        403: {"description": "Forbidden. User is not a team participant."},
        404: {"description": "Team not found."}
    }
)

router.add_api_route(
    '/teams/{team_id}',
    delete_team,
    methods=['DELETE'],
    dependencies=[Depends(http_bearer)],
    status_code=200,
    responses={
        200: {"description": "Successfully deleted the team", "model": TeamResponse},
        401: {"description": "Unauthorized. User not authenticated."},
        403: {"description": "Forbidden. User is not the team owner."},
        404: {"description": "Team not found."}
    }
)

router.add_api_route(
    '/teams',
    create_team,
    methods=["POST"],
    dependencies=[Depends(http_bearer)],
    status_code=201,
    responses={
        201: {"description": "Successfully created the team", "model": TeamResponse},
        401: {"description": "Unauthorized. User not authenticated."}
    }
)

router.add_api_route(
    '/teams/{team_id}/participant/{user_id}',
    add_team_participant,
    methods=["PUT"],
    dependencies=[Depends(http_bearer)],
    status_code=200,
    responses={
        200: {"description": "Successfully added user to the team", "model": TeamResponse},
        401: {"description": "Unauthorized. User not authenticated."},
        403: {"description": "Forbidden. User is not the team owner."}
    }
)

router.add_api_route(
    '/teams/{team_id}/participant/{user_id}',
    remove_team_participant,
    methods=["DELETE"],
    dependencies=[Depends(http_bearer)],
    status_code=200,
    responses={
        200: {"description": "Successfully removed user from the team", "model": TeamResponse},
        401: {"description": "Unauthorized. User not authenticated."},
        400: {"description": "Bad request. Cannot remove team owner."},
        403: {"description": "Forbidden. User is not the team owner."}
    }
)
