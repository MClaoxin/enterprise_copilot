from typing import Literal
from uuid import UUID

from app.core.exceptions import WorkspaceForbiddenError
from app.repositories.workspace_member import WorkspaceMemberRepository

WorkspaceRole = Literal["owner", "admin", "member", "viewer"]
ROLE_LEVEL = {"viewer": 10, "member": 20, "admin": 30, "owner": 40}


class AuthorizationService:
    def __init__(self, members: WorkspaceMemberRepository):
        self.members = members

    def require_role(
        self, workspace_id: UUID, user_id: UUID, minimum: WorkspaceRole
    ) -> None:
        member = self.members.get(workspace_id, user_id)
        if member is None or ROLE_LEVEL.get(member.role, 0) < ROLE_LEVEL[minimum]:
            raise WorkspaceForbiddenError()
