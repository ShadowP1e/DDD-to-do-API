from dependency_injector import containers, providers

from core.database.postgres.database import SessionLocal
from core.event_dispatcher import EventDispatcher
from features.auth.application.use_cases.login_user import LoginUserUseCase
from features.auth.application.use_cases.refresh_token import RefreshTokenUseCase
from features.auth.infrastructure.providers.current_user_provider import CurrentUserProvider
from features.auth.infrastructure.strategies.jwt_auth_strategy import JWTAuthStrategy
from features.task.application.use_cases.assign_task import AssignTaskUseCase
from features.task.application.use_cases.create_task import CreateTaskUseCase
from features.task.application.use_cases.delete_task import DeleteTaskUseCase
from features.task.application.use_cases.get_task import GetTaskUseCase
from features.task.application.use_cases.get_team_tasks import GetTeamTasksUseCase
from features.task.application.use_cases.unassign_task import UnassignTaskUseCase
from features.task.infrastructure.repositories.task_unit_of_work_impl import SQLAlchemyTaskUnitOfWorkImpl
from features.task.infrastructure.services.task_query_service_impl import SQLAlchemyTaskQueryServiceImpl
from features.team.application.use_cases.add_team_participant import AddTeamParticipantUseCase
from features.team.application.use_cases.create_team import CreateTeamUseCase
from features.team.application.use_cases.delete_team import DeleteTeamUseCase
from features.team.application.use_cases.get_team import GetTeamUseCase
from features.team.application.use_cases.get_user_teams import GetTeamsWithUserUseCase
from features.team.application.use_cases.remove_team_participant import RemoveTeamParticipantUseCase
from features.team.infrastructure.repositories.team_unit_of_work_impl import SQLAlchemyTeamUnitOfWorkImpl
from features.team.infrastructure.services.team_query_service_impl import SQLAlchemyTeamQueryServiceImpl
from features.user.application.use_cases.create_user import CreateUserUseCase
from features.user.application.use_cases.get_user import GetUserUseCase
from features.user.infrastructure.repositories.user_unit_of_work_impl import SQLAlchemyUserUnitOfWorkImpl
from features.user.infrastructure.services.logging_service import LoggingService
from features.user.infrastructure.services.user_query_service_impl import SQLAlchemyUserQueryServiceImpl


class Container(containers.DeclarativeContainer):
    # Database session
    session = providers.Factory(SessionLocal)
    session_factory = providers.Resource(lambda: SessionLocal)

    # Auth
    jwt_auth_strategy = providers.Factory(
        JWTAuthStrategy,
        jwt_secret_key='secret',
        jwt_algorithm='HS256'
    )

    current_user_provider = providers.Factory(
        CurrentUserProvider,
        auth_strategy=jwt_auth_strategy,
    )

    # Services
    user_query_service = providers.Factory(
        SQLAlchemyUserQueryServiceImpl,
        session_factory=session_factory,
    )
    team_query_service = providers.Factory(
        SQLAlchemyTeamQueryServiceImpl,
        session_factory=session_factory,
    )
    task_query_service = providers.Factory(
        SQLAlchemyTaskQueryServiceImpl,
        session_factory=session_factory,
    )
    logging_service = providers.Singleton(LoggingService)

    # Event dispatcher
    event_dispatcher = providers.Singleton(
        EventDispatcher,
        handlers={}
    )

    # Unit of Work
    user_uow = providers.Factory(
        SQLAlchemyUserUnitOfWorkImpl,
        session=session,
    )
    team_uow = providers.Factory(
        SQLAlchemyTeamUnitOfWorkImpl,
        session=session,
    )
    task_uow = providers.Factory(
        SQLAlchemyTaskUnitOfWorkImpl,
        session=session,
    )

    # Use cases
    # --- Users ---
    create_user_use_case = providers.Factory(
        CreateUserUseCase,
        uow=user_uow,
        event_dispatcher=event_dispatcher,
    )
    get_user_use_case = providers.Factory(
        GetUserUseCase,
        service=user_query_service,
        event_dispatcher=event_dispatcher,
    )
    # --- Auth ---
    refresh_token_use_case = providers.Factory(
        RefreshTokenUseCase,
        auth_strategy=jwt_auth_strategy,
    )
    login_user_use_case = providers.Factory(
        LoginUserUseCase,
        auth_strategy=jwt_auth_strategy,
        user_query_service=user_query_service
    )
    # --- Teams ---
    create_team_use_case = providers.Factory(
        CreateTeamUseCase,
        uow=team_uow,
        event_dispatcher=event_dispatcher
    )
    delete_team_use_case = providers.Factory(
        DeleteTeamUseCase,
        uow=team_uow,
        event_dispatcher=event_dispatcher
    )
    add_team_participant_use_case = providers.Factory(
        AddTeamParticipantUseCase,
        uow=team_uow,
        event_dispatcher=event_dispatcher
    )
    remove_team_participant_use_case = providers.Factory(
        RemoveTeamParticipantUseCase,
        uow=team_uow,
        event_dispatcher=event_dispatcher
    )
    get_team_use_case = providers.Factory(
        GetTeamUseCase,
        service=team_query_service,
        event_dispatcher=event_dispatcher
    )
    get_teams_with_user_use_case = providers.Factory(
        GetTeamsWithUserUseCase,
        service=team_query_service,
        event_dispatcher=event_dispatcher
    )
    # --- Tasks ---
    create_task_use_case = providers.Factory(
        CreateTaskUseCase,
        uow=task_uow,
        event_dispatcher=event_dispatcher,
    )
    get_team_tasks_use_case = providers.Factory(
        GetTeamTasksUseCase,
        service=task_query_service,
        event_dispatcher=event_dispatcher,
    )
    get_task_use_case = providers.Factory(
        GetTaskUseCase,
        service=task_query_service,
        event_dispatcher=event_dispatcher,
    )
    delete_task_use_case = providers.Factory(
        DeleteTaskUseCase,
        uow=task_uow,
        event_dispatcher=event_dispatcher,
    )
    assign_task_use_case = providers.Factory(
        AssignTaskUseCase,
        uow=task_uow,
        event_dispatcher=event_dispatcher,
    )
    unassign_task_use_case = providers.Factory(
        UnassignTaskUseCase,
        uow=task_uow,
        event_dispatcher=event_dispatcher,
    )
