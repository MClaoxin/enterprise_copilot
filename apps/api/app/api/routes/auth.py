from fastapi import APIRouter, status

from app.api.deps import AuthServiceDep, CurrentUserDep, UserServiceDep
from app.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    RegisterResponse,
    TokenPair,
)
from app.schemas.user import UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED
)
async def register(data: RegisterRequest, users: UserServiceDep, auth: AuthServiceDep):
    user = users.create_user(data)
    return RegisterResponse(user=user, tokens=auth.issue_tokens(user))


@router.post("/login", response_model=TokenPair)
async def login(data: LoginRequest, auth: AuthServiceDep):
    return auth.issue_tokens(auth.authenticate(data.email, data.password))


@router.post("/refresh", response_model=TokenPair)
async def refresh(data: RefreshRequest, auth: AuthServiceDep):
    return auth.refresh(data.refresh_token)


@router.get("/me", response_model=UserResponse)
async def me(current_user: CurrentUserDep):
    return current_user
