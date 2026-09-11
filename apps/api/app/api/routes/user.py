from fastapi import APIRouter, HTTPException, status

from app.schemas.user import UserCreate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

fake_users = {
    1: {"id": 1, "name": "John Doe", "email": "john.doe@example.com"}
}

@router.get("", response_model=list[UserResponse])
async def list_users(
    page: int = 1,
    page_size: int = 10
):
    users = list(fake_users.values())
    start = (page - 1) * page_size
    end = start + page_size
    return users[start:end]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = fake_users.get(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    new_id = max(fake_users.keys(), default=0) + 1
    new_user = {"id": new_id, **user.model_dump()}
    fake_users[new_id] = new_user
    return new_user