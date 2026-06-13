"""Authentication API endpoints."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

from app.api.deps import get_current_user
from app.services.auth_service import get_auth_service, AuthService

router = APIRouter()


# Request/Response models
class RegisterRequest(BaseModel):
    """User registration request."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    name: Optional[str] = Field(None, max_length=255)


class LoginRequest(BaseModel):
    """User login request."""

    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    """Token refresh request."""

    refresh_token: str


class TokenResponse(BaseModel):
    """Token response with user info."""

    user: dict
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AccessTokenResponse(BaseModel):
    """Access token only response."""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User profile response."""

    id: str
    email: str
    name: Optional[str] = None


@router.post("/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """
    Register a new user account.

    Returns access and refresh tokens on success.
    """
    try:
        result = await auth_service.register_user(
            email=request.email,
            password=request.password,
            name=request.name,
        )
        return TokenResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/auth/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """
    Authenticate user and get tokens.

    Returns access and refresh tokens on success.
    """
    try:
        result = await auth_service.authenticate_user(
            email=request.email,
            password=request.password,
        )
        return TokenResponse(**result)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )


@router.post("/auth/refresh", response_model=AccessTokenResponse)
async def refresh_token(
    request: RefreshRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> AccessTokenResponse:
    """
    Refresh access token using refresh token.

    Returns new access token on success.
    """
    try:
        result = await auth_service.refresh_access_token(request.refresh_token)
        return AccessTokenResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.get("/auth/me", response_model=UserResponse)
async def get_me(
    current_user: dict = Depends(get_current_user),
) -> UserResponse:
    """
    Get current authenticated user profile.

    Requires Bearer token authentication.
    """
    return UserResponse(
        id=str(current_user["id"]),
        email=current_user["email"],
        name=current_user.get("name"),
    )
