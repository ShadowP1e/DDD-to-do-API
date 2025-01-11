from fastapi import APIRouter

from features.auth.presentation.v1.endpoints.login_user import login_user
from features.auth.presentation.v1.endpoints.refresh_token import refresh_token
from features.auth.presentation.v1.schemas import TokensResponse

router = APIRouter(prefix='/api/v1', tags=['auth'])

router.add_api_route(
    '/auth/login',
    login_user,
    methods=["POST"],
    status_code=200,
    responses={
        200: {"description": "Login successful", "model": TokensResponse},
        400: {"description": "Bad request. Invalid input data."},
        403: {"description": "Forbidden. Invalid credentials."}
    }
)

router.add_api_route(
    '/auth/refresh',
    refresh_token,
    methods=["POST"],
    status_code=200,
    responses={
        200: {"description": "Token refreshed successfully", "model": TokensResponse},
        400: {"description": "Bad request. Invalid input data."},
        401: {"description": "Unauthorized. Invalid refresh token."}
    }
)
