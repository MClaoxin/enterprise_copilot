from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health", headers={"X-Request-ID": "health-check"})

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "health-check"
    assert response.json() == {
        "status": "ok",
        "service": "Enterprise Copilot API",
    }
