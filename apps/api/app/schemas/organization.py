from uuid import UUID
from pydantic import BaseModel, Field


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)


class OrganizationUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)


class OrganizationResponse(BaseModel):
    id: UUID
    name: str