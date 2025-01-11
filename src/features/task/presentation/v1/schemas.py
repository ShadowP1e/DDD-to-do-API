from datetime import datetime

from pydantic import BaseModel

from features.user.presentation.v1.schemas import UserResponse


class CreateTaskRequest(BaseModel):
    title: str
    description: str
    deadline: datetime


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    team_id: int
    creator_id: int
    assignee_id: int | None = None
    creator: UserResponse
    assignee: UserResponse | None = None
    deadline: datetime | None = None
