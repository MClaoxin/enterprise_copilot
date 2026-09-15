from types import SimpleNamespace
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from app.api.deps import get_workspace_service
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

    def list_workspaces(self):
        return list(self.workspaces.values())

    def get_workspace(self, workspace_id: UUID):
        if workspace_id not in self.workspaces:
            raise WorkspaceNotFoundError()
        return self.workspaces[workspace_id]

    def create_workspace(self, data):
        workspace = SimpleNamespace(id=uuid4(), **data.model_dump())
        self.workspaces[workspace.id] = workspace
        return workspace


service = FakeWorkspaceService()
app.dependency_overrides[get_workspace_service] = lambda: service
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
            "owner_id": str(service.owner_id),
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "New Workspace"
