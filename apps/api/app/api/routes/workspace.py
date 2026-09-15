from uuid import UUID

from fastapi import APIRouter, Response, status

from app.api.deps import AuthorizationServiceDep, CurrentUserDep, WorkspaceServiceDep
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse, WorkspaceUpdate

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


@router.get("", response_model=list[WorkspaceResponse])
async def list_workspaces(service: WorkspaceServiceDep, current_user: CurrentUserDep):
    return service.list_workspaces(current_user.id)


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(
    workspace_id: UUID,
    service: WorkspaceServiceDep,
    current_user: CurrentUserDep,
    authorization: AuthorizationServiceDep,
):
    authorization.require_role(workspace_id, current_user.id, "viewer")
    return service.get_workspace(workspace_id)


@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    data: WorkspaceCreate, service: WorkspaceServiceDep, current_user: CurrentUserDep
):
    return service.create_workspace(data, current_user.id)


@router.patch("/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace(
    workspace_id: UUID,
    data: WorkspaceUpdate,
    service: WorkspaceServiceDep,
    current_user: CurrentUserDep,
    authorization: AuthorizationServiceDep,
):
    authorization.require_role(workspace_id, current_user.id, "admin")
    return service.update_workspace(workspace_id, data)


@router.delete("/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workspace(
    workspace_id: UUID,
    service: WorkspaceServiceDep,
    current_user: CurrentUserDep,
    authorization: AuthorizationServiceDep,
):
    authorization.require_role(workspace_id, current_user.id, "owner")
    service.delete_workspace(workspace_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
