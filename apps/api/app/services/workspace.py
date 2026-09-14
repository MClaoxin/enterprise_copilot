from uuid import UUID

from app.core.exceptions import (
    WorkspaceAlreadyExistsError,
    WorkspaceNotFoundError,
)

from app.models.workspace import Workspace
from app.repositories.workspace import WorkspaceRepository
from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate

class WorkspaceService:

    def __init__(
        self,
        repository: WorkspaceRepository,
    ):
        self.repository = repository

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
        existing = self.repository.get_by_name(
            data.name
        )

        if existing:
            raise WorkspaceAlreadyExistsError()

        workspace = self.repository.create(data)

        self.repository.db.commit()
        self.repository.db.refresh(workspace)

        return workspace

    def update_workspace(
        self,
        workspace_id: UUID,
        data: WorkspaceUpdate,
    ) -> Workspace:
        workspace = self.get_workspace(workspace_id)
        return self.repository.update(workspace, data)

    def delete_workspace(
        self,
        workspace_id: UUID,
    ) -> None:
        workspace = self.get_workspace(workspace_id)
        self.repository.delete(workspace)
        self.repository.db.commit()