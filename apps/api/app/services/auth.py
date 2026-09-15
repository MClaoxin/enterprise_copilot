from datetime import timedelta

from app.core.config import settings
from app.core.exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
    InvalidTokenError,
)
from app.core.security import create_token, decode_token, verify_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import TokenPair


class AuthService:
    def __init__(self, users: UserRepository):
        self.users = users

    def authenticate(self, email: str, password: str) -> User:
        user = self.users.get_by_email(email)
        if user is None or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()
        if not user.is_active:
            raise InactiveUserError()
        return user

    def issue_tokens(self, user: User) -> TokenPair:
        return TokenPair(
            access_token=create_token(
                user.id,
                "access",
                timedelta(minutes=settings.access_token_expire_minutes),
            ),
            refresh_token=create_token(
                user.id,
                "refresh",
                timedelta(days=settings.refresh_token_expire_days),
            ),
        )

    def refresh(self, refresh_token: str) -> TokenPair:
        user_id = decode_token(refresh_token, "refresh")
        user = self.users.get_by_id(user_id)
        if user is None:
            raise InvalidTokenError()
        if not user.is_active:
            raise InactiveUserError()
        return self.issue_tokens(user)

    def current_user(self, access_token: str) -> User:
        user_id = decode_token(access_token, "access")
        user = self.users.get_by_id(user_id)
        if user is None:
            raise InvalidTokenError()
        if not user.is_active:
            raise InactiveUserError()
        return user
