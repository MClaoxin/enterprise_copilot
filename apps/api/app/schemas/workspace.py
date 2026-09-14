from uuid import UUID
from pydantic import BaseModel, Field

class WorkspaceCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    organization_id: UUID


class WorkspaceUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )


class WorkspaceResponse(BaseModel):
    id: UUID
    name: str
    organization_id: UUID 