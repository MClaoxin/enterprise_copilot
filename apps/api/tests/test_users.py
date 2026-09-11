from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_list_users():
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_user():
    response = client.get("/api/v1/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_user_not_found():
    response = client.get("/api/v1/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_create_user():
    response = client.post("/api/v1/users", json={"name": "Jane Doe", "email": "jane.doe@example.com"})
    assert response.status_code == 201
    assert response.json()["name"] == "Jane Doe"