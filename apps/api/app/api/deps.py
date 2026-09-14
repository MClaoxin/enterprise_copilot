from typing import Annotated

from fastapi import Depends

from app.db.session import get_db
from app.repositories.user import UserRepository
from app.repositories.workspace import WorkspaceRepository
from app.services.user import UserService
from app.services.workspace import WorkspaceService

DBSessionDep = Annotated[object, Depends(get_db)]


def get_user_repository(
    db: DBSessionDep,
) -> UserRepository:
    return UserRepository(db)


UserRepositoryDep = Annotated[
    UserRepository,
    Depends(get_user_repository),
]


def get_user_service(
    repository: UserRepositoryDep,
) -> UserService:
    return UserService(repository)


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


def get_workspace_service(
    repository: WorkspaceRepositoryDep,
) -> WorkspaceService:
    return WorkspaceService(repository)


WorkspaceServiceDep = Annotated[
    WorkspaceService,
    Depends(get_workspace_service),
]
