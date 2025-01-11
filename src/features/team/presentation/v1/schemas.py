from pydantic import BaseModel

from features.user.presentation.v1.schemas import CreateUserRequest, UserResponse


class CreateTeamRequest(BaseModel):
    name: str


class TeamResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    owner: UserResponse
    participants: list[UserResponse]
