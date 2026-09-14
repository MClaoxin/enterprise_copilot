from uuid import UUID

from fastapi import APIRouter, Response, status

from app.api.deps import WorkspaceServiceDep
from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse

router = APIRouter(
    prefix="/workspaces",
    tags=["workspaces"]
)


@router.get("", response_model=list[WorkspaceResponse])
async def list_workspaces(service: WorkspaceServiceDep):
    return service.list_workspaces()

@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(workspace_id: UUID, service: WorkspaceServiceDep):
    return service.get_workspace(workspace_id)

@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(data: WorkspaceCreate, service: WorkspaceServiceDep):
    return service.create_workspace(data)

@router.patch("/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace(workspace_id: UUID, data: WorkspaceUpdate, service: WorkspaceServiceDep):
    return service.update_workspace(workspace_id, data)

@router.delete("/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workspace(workspace_id: UUID, service: WorkspaceServiceDep):
    service.delete_workspace(workspace_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)