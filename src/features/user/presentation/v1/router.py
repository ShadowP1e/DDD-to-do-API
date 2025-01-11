from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import HTTPBearer

from features.user.presentation.v1.endpoints.create_user import create_user
from features.user.presentation.v1.endpoints.get_user import get_current_user
from features.user.presentation.v1.schemas import UserResponse

http_bearer = HTTPBearer(auto_error=False)  # Only for openapi.json

router = APIRouter(prefix='/api/v1', tags=['users'])

router.add_api_route(
    '/users',
    create_user,
    methods=["POST"],
    status_code=201,
    responses={
        201: {"description": "User created successfully", "model": UserResponse},
        400: {"description": "Bad request. Invalid input data."},
        409: {"description": "Conflict. User already exists."}
    }
)

router.add_api_route(
    '/users/me',
    get_current_user,
    methods=["GET"],
    dependencies=[Depends(http_bearer)],
    status_code=200,
    responses={
        200: {"description": "User details retrieved successfully", "model": UserResponse},
        401: {"description": "Unauthorized. Invalid credentials."},
        404: {"description": "Not found. User does not exist."}
    }
)
