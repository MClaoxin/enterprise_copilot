from types import SimpleNamespace
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from app.api.deps import get_user_service
from app.main import app


class FakeUserService:
    def __init__(self):
        self.user_id = uuid4()
        self.users = {
            self.user_id: SimpleNamespace(
                id=self.user_id,
                name="John Doe",
                email="john@example.com",
            )
        }

    def list_users(self):
        return list(self.users.values())

    def get_user(self, user_id: UUID):
        from app.core.exceptions import UserNotFoundError

        if user_id not in self.users:
            raise UserNotFoundError()
        return self.users[user_id]

    def create_user(self, data):
        user = SimpleNamespace(id=uuid4(), name=data.name, email=data.email)
        self.users[user.id] = user
        return user


service = FakeUserService()
app.dependency_overrides[get_user_service] = lambda: service
client = TestClient(app, raise_server_exceptions=False)


def test_list_users():
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_user():
    response = client.get(f"/api/v1/users/{service.user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == str(service.user_id)


def test_get_user_not_found():
    response = client.get(f"/api/v1/users/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "USER_NOT_FOUND"


def test_create_user():
    response = client.post(
        "/api/v1/users",
        json={
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "password": "secure-password",
        },
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Jane Doe"
