from uuid import UUID

from app.core.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:

    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository

    def get_user(
        self,
        user_id: UUID,
    ) -> User:
        user = self.repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError()

        return user

    def list_users(self) -> list[User]:
        return self.repository.list()

    def create_user(
        self,
        data: UserCreate,
    ) -> User:
        existing = self.repository.get_by_email(
            data.email
        )

        if existing:
            raise UserAlreadyExistsError()

        # Day 5 暂时表示
        password_hash = f"hashed:{data.password}"

        user = self.repository.create(
            data,
            password_hash,
        )

        self.repository.db.commit()
        self.repository.db.refresh(user)

        return user

    def update_user(
        self,
        user_id: UUID,
        data: UserUpdate,
    ) -> User:

        user = self.get_user(user_id)

        user = self.repository.update(
            user,
            data,
        )

        self.repository.db.commit()
        self.repository.db.refresh(user)

        return user

    def delete_user(
        self,
        user_id: UUID,
    ) -> None:
        user = self.get_user(user_id)

        self.repository.delete(user)
        self.repository.db.commit()