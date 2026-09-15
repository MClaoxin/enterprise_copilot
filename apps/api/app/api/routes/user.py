from uuid import UUID

from fastapi import APIRouter, Response, status

from app.api.deps import UserServiceDep
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("", response_model=list[UserResponse])
async def list_users( service: UserServiceDep,):
    return service.list_users()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, service: UserServiceDep):
    return service.get_user(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: UUID, data: UserUpdate, service: UserServiceDep):
    return service.update_user(user_id, data)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, service: UserServiceDep):
    return service.create_user(data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, service: UserServiceDep):
    service.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)