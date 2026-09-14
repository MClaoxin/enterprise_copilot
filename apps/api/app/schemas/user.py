from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    email: EmailStr


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr