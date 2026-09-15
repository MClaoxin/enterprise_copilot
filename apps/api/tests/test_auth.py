from datetime import timedelta
from types import SimpleNamespace
from uuid import uuid4

import pytest

from app.core.config import settings
from app.core.exceptions import InvalidCredentialsError, InvalidTokenError
from app.core.security import create_token, decode_token, hash_password, verify_password
from app.services.auth import AuthService


def test_password_is_hashed_and_verifiable():
    encoded = hash_password("correct horse battery staple")
    assert encoded != "correct horse battery staple"
    assert verify_password("correct horse battery staple", encoded)
    assert not verify_password("wrong password", encoded)


def test_access_and_refresh_tokens_are_not_interchangeable(monkeypatch):
    monkeypatch.setattr(
        settings, "jwt_secret_key", "test-key-with-at-least-thirty-two-bytes"
    )
    user_id = uuid4()
    refresh = create_token(user_id, "refresh", timedelta(minutes=5))
    assert decode_token(refresh, "refresh") == user_id
    with pytest.raises(InvalidTokenError):
        decode_token(refresh, "access")


def test_authentication_rejects_wrong_password():
    user = SimpleNamespace(
        id=uuid4(),
        hashed_password=hash_password("correct-password"),
        is_active=True,
    )
    repository = SimpleNamespace(get_by_email=lambda email: user)
    service = AuthService(repository)

    with pytest.raises(InvalidCredentialsError):
        service.authenticate("user@example.com", "wrong-password")
