from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.unit_of_work import UnitOfWork
from app.repositories.user import UserRepository
from app.repositories.workspace import WorkspaceRepository
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


def get_workspace_service(
    repository: WorkspaceRepositoryDep,
    unit_of_work: UnitOfWorkDep,
) -> WorkspaceService:
    return WorkspaceService(repository, unit_of_work)


WorkspaceServiceDep = Annotated[
    WorkspaceService,
    Depends(get_workspace_service),
]
