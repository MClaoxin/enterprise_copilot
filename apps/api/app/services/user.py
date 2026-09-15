from uuid import UUID

from sqlalchemy.exc import IntegrityError

from app.core.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.core.security import hash_password
from app.db.unit_of_work import UnitOfWork
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(
        self,
        repository: UserRepository,
        unit_of_work: UnitOfWork,
    ):
        self.repository = repository
        self.unit_of_work = unit_of_work

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
        existing = self.repository.get_by_email(data.email)

        if existing:
            raise UserAlreadyExistsError()

        hashed_password = hash_password(data.password)

        try:
            user = self.repository.create(data, hashed_password)
            self.unit_of_work.commit()
        except IntegrityError as exc:
            self.unit_of_work.rollback()
            raise UserAlreadyExistsError() from exc
        self.unit_of_work.refresh(user)

        return user

    def update_user(
        self,
        user_id: UUID,
        data: UserUpdate,
    ) -> User:

        user = self.get_user(user_id)

        user = self.repository.update(user, data)
        self.unit_of_work.commit()
        self.unit_of_work.refresh(user)

        return user

    def delete_user(
        self,
        user_id: UUID,
    ) -> None:
        user = self.get_user(user_id)

        self.repository.delete(user)
        self.unit_of_work.commit()
