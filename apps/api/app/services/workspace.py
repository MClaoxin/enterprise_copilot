from uuid import UUID

from sqlalchemy.exc import IntegrityError

from app.core.exceptions import (
    WorkspaceAlreadyExistsError,
    WorkspaceNotFoundError,
)
from app.db.unit_of_work import UnitOfWork
from app.models.workspace import Workspace
from app.repositories.workspace import WorkspaceRepository
from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate


class WorkspaceService:
    def __init__(
        self,
        repository: WorkspaceRepository,
        unit_of_work: UnitOfWork,
    ):
        self.repository = repository
        self.unit_of_work = unit_of_work

    def get_workspace(
        self,
        workspace_id: UUID,
    ) -> Workspace:
        workspace = self.repository.get_by_id(workspace_id)

        if workspace is None:
            raise WorkspaceNotFoundError()

        return workspace

    def list_workspaces(self) -> list[Workspace]:
        return self.repository.list()

    def create_workspace(
        self,
        data: WorkspaceCreate,
    ) -> Workspace:
        existing = self.repository.get_by_slug(data.slug)

        if existing:
            raise WorkspaceAlreadyExistsError()

        try:
            workspace = self.repository.create(data)
            self.unit_of_work.commit()
        except IntegrityError as exc:
            self.unit_of_work.rollback()
            raise WorkspaceAlreadyExistsError() from exc
        self.unit_of_work.refresh(workspace)

        return workspace

    def update_workspace(
        self,
        workspace_id: UUID,
        data: WorkspaceUpdate,
    ) -> Workspace:
        workspace = self.get_workspace(workspace_id)
        try:
            workspace = self.repository.update(workspace, data)
            self.unit_of_work.commit()
        except IntegrityError as exc:
            self.unit_of_work.rollback()
            raise WorkspaceAlreadyExistsError() from exc
        self.unit_of_work.refresh(workspace)
        return workspace

    def delete_workspace(
        self,
        workspace_id: UUID,
    ) -> None:
        workspace = self.get_workspace(workspace_id)
        self.repository.delete(workspace)
        self.unit_of_work.commit()
