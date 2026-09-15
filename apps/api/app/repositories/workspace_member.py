from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workspace_member import WorkspaceMember


class WorkspaceMemberRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, workspace_id: UUID, user_id: UUID) -> WorkspaceMember | None:
        return self.db.scalar(
            select(WorkspaceMember).where(
                WorkspaceMember.workspace_id == workspace_id,
                WorkspaceMember.user_id == user_id,
            )
        )

    def add(self, workspace_id: UUID, user_id: UUID, role: str) -> WorkspaceMember:
        member = WorkspaceMember(workspace_id=workspace_id, user_id=user_id, role=role)
        self.db.add(member)
        self.db.flush()
        return member
