from fastapi import FastAPI

from container import Container
from features.auth.presentation.v1 import endpoints as v1_auth_endpoints
from features.auth.presentation.v1.router import router as v1_auth_router
from features.team.presentation.v1 import endpoints as v1_team_endpoints
from features.team.presentation.v1.router import router as v1_team_router
from features.user.presentation.v1 import endpoints as v1_user_endpoints
from features.user.presentation.v1.router import router as v1_user_router
from features.task.presentation.v1 import endpoints as v1_task_endpoints
from features.task.presentation.v1.router import router as v1_task_router

app = FastAPI()

app.include_router(v1_user_router)
app.include_router(v1_auth_router)
app.include_router(v1_team_router)
app.include_router(v1_task_router)

container = Container()
container.wire(packages=[v1_user_endpoints, v1_auth_endpoints, v1_team_endpoints, v1_task_endpoints])
