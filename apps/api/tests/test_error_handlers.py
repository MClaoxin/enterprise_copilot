import logging

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.error_handlers import register_exception_handlers
from app.core.exceptions import UserNotFoundError
from app.core.middleware import RequestLoggingMiddleware


def create_test_app() -> FastAPI:
    test_app = FastAPI()
    test_app.add_middleware(RequestLoggingMiddleware)
    register_exception_handlers(test_app)

    @test_app.get("/business-error")
    async def business_error():
        raise UserNotFoundError()

    @test_app.get("/unexpected-error")
    async def unexpected_error():
        raise RuntimeError("sensitive detail")

    @test_app.get("/items/{item_id}")
    async def get_item(item_id: int):
        return {"item_id": item_id}

    return test_app


client = TestClient(create_test_app(), raise_server_exceptions=False)


def test_app_exception_has_consistent_response_and_request_id():
    response = client.get("/business-error", headers={"X-Request-ID": "test-request"})

    assert response.status_code == 404
    assert response.headers["X-Request-ID"] == "test-request"
    assert response.json() == {
        "error": {"code": "USER_NOT_FOUND", "message": "User not found"},
        "request_id": "test-request",
    }


def test_validation_exception_uses_consistent_response():
    response = client.get("/items/not-an-integer")

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
    assert response.json()["error"]["details"]


def test_unhandled_exception_is_logged_without_leaking_details(caplog):
    with caplog.at_level(logging.ERROR):
        response = client.get("/unexpected-error")

    assert response.status_code == 500
    assert response.json()["error"]["code"] == "INTERNAL_SERVER_ERROR"
    assert "sensitive detail" not in response.text
    assert "Request failed" in caplog.text
