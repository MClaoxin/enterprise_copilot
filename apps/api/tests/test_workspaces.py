from types import SimpleNamespace
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from app.api.deps import (
    get_authorization_service,
    get_current_user,
    get_workspace_service,
)
from app.core.exceptions import WorkspaceNotFoundError
from app.main import app


class FakeWorkspaceService:
    def __init__(self):
        self.owner_id = uuid4()
        self.workspace_id = uuid4()
        self.workspaces = {
            self.workspace_id: SimpleNamespace(
                id=self.workspace_id,
                name="Demo Workspace",
                slug="demo-workspace",
                owner_id=self.owner_id,
            )
        }

    def list_workspaces(self, user_id):
        return list(self.workspaces.values())

    def get_workspace(self, workspace_id: UUID):
        if workspace_id not in self.workspaces:
            raise WorkspaceNotFoundError()
        return self.workspaces[workspace_id]

    def create_workspace(self, data, owner_id):
        workspace = SimpleNamespace(id=uuid4(), owner_id=owner_id, **data.model_dump())
        self.workspaces[workspace.id] = workspace
        return workspace


service = FakeWorkspaceService()
app.dependency_overrides[get_workspace_service] = lambda: service
app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
    id=service.owner_id
)
app.dependency_overrides[get_authorization_service] = lambda: SimpleNamespace(
    require_role=lambda *args: None
)
client = TestClient(app, raise_server_exceptions=False)


def test_list_workspaces():
    response = client.get("/api/v1/workspaces")

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Demo Workspace"


def test_get_workspace_not_found():
    response = client.get(f"/api/v1/workspaces/{uuid4()}")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "WORKSPACE_NOT_FOUND"


def test_create_workspace():
    response = client.post(
        "/api/v1/workspaces",
        json={
            "name": "New Workspace",
            "slug": "new-workspace",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "New Workspace"
