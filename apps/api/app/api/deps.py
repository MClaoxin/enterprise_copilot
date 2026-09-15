from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.unit_of_work import UnitOfWork
from app.models.user import User
from app.repositories.user import UserRepository
from app.repositories.workspace import WorkspaceRepository
from app.repositories.workspace_member import WorkspaceMemberRepository
from app.services.auth import AuthService
from app.services.authorization import AuthorizationService
from app.services.user import UserService
from app.services.workspace import WorkspaceService

DBSessionDep = Annotated[Session, Depends(get_db)]


def get_unit_of_work(db: DBSessionDep) -> UnitOfWork:
    return UnitOfWork(db)


UnitOfWorkDep = Annotated[UnitOfWork, Depends(get_unit_of_work)]


def get_user_repository(
    db: DBSessionDep,
) -> UserRepository:
    return UserRepository(db)


UserRepositoryDep = Annotated[
    UserRepository,
    Depends(get_user_repository),
]


def get_auth_service(repository: UserRepositoryDep) -> AuthService:
    return AuthService(repository)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    auth: AuthServiceDep,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
):
    from app.core.exceptions import InvalidTokenError

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise InvalidTokenError()
    return auth.current_user(credentials.credentials)


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def get_user_service(
    repository: UserRepositoryDep,
    unit_of_work: UnitOfWorkDep,
) -> UserService:
    return UserService(repository, unit_of_work)


UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service),
]


def get_workspace_repository(
    db: DBSessionDep,
) -> WorkspaceRepository:
    return WorkspaceRepository(db)


WorkspaceRepositoryDep = Annotated[
    WorkspaceRepository,
    Depends(get_workspace_repository),
]


def get_workspace_member_repository(db: DBSessionDep) -> WorkspaceMemberRepository:
    return WorkspaceMemberRepository(db)


WorkspaceMemberRepositoryDep = Annotated[
    WorkspaceMemberRepository, Depends(get_workspace_member_repository)
]


def get_authorization_service(
    members: WorkspaceMemberRepositoryDep,
) -> AuthorizationService:
    return AuthorizationService(members)


AuthorizationServiceDep = Annotated[
    AuthorizationService, Depends(get_authorization_service)
]


def get_workspace_service(
    repository: WorkspaceRepositoryDep,
    unit_of_work: UnitOfWorkDep,
    members: WorkspaceMemberRepositoryDep,
) -> WorkspaceService:
    return WorkspaceService(repository, unit_of_work, members)


WorkspaceServiceDep = Annotated[
    WorkspaceService,
    Depends(get_workspace_service),
]
