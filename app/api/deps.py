"""FastAPI dependencies for authentication."""

from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.services.auth_service import get_auth_service, AuthService

# Security scheme
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    """
    Get current authenticated user from Bearer token.
    Raises 401 if not authenticated.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await auth_service.get_user_from_token(credentials.credentials)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    auth_service: AuthService = Depends(get_auth_service),
) -> Optional[dict]:
    """
    Get current user if authenticated, None otherwise.
    Use for routes that work with or without authentication.
    """
    if not credentials:
        return None

    return await auth_service.get_user_from_token(credentials.credentials)


def get_user_id(user: dict = Depends(get_current_user)) -> UUID:
    """Extract user ID from authenticated user."""
    return user["id"]


def get_user_id_optional(
    user: Optional[dict] = Depends(get_current_user_optional),
) -> Optional[UUID]:
    """Extract user ID if authenticated."""
    return user["id"] if user else None
