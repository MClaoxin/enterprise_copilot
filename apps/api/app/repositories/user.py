from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: UUID) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.scalar(stmt)

    def list(
            self,
            offset: int = 0,
            limit: int = 20,
    ) -> list[User]:
        stmt = select(User).offset(offset).limit(limit)
        return list(self.db.scalars(stmt).all())

    def create(self, data: UserCreate, password_hash: str) -> User:
        user = User(
            email=data.email,
            name=data.name,
            password_hash=password_hash,
        )
        self.db.add(user)
        self.db.flush()
        return user

    def update(self, user: User, data: UserUpdate) -> User:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(user, field, value)

        self.db.flush()

        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)