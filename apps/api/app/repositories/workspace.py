from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workspace import Workspace
from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate


class WorkspaceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, workspace_id: UUID) -> Workspace | None:
        return self.db.get(Workspace, workspace_id)

    def list(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Workspace]:
        stmt = select(Workspace).offset(offset).limit(limit)
        return list(self.db.scalars(stmt).all())

    def get_by_slug(self, slug: str) -> Workspace | None:
        stmt = select(Workspace).where(Workspace.slug == slug)
        return self.db.scalar(stmt)

    def create(self, data: WorkspaceCreate) -> Workspace:
        workspace = Workspace(
            name=data.name,
            slug=data.slug,
            owner_id=data.owner_id,
        )
        self.db.add(workspace)
        self.db.flush()
        return workspace

    def update(self, workspace: Workspace, data: WorkspaceUpdate) -> Workspace:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(workspace, field, value)

        self.db.flush()

        return workspace

    def delete(self, workspace: Workspace) -> None:
        self.db.delete(workspace)
