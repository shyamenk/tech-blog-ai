"""Authentication service for JWT token management."""

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import get_settings
from app.db.repositories import UserRepository

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service for authentication operations."""

    def __init__(self):
        self.settings = get_settings()

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, user_id: UUID, email: str) -> str:
        """Create a JWT access token."""
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.settings.jwt_access_token_expire_minutes
        )
        payload = {
            "sub": str(user_id),
            "email": email,
            "type": "access",
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(
            payload,
            self.settings.jwt_secret_key,
            algorithm=self.settings.jwt_algorithm,
        )

    def create_refresh_token(self, user_id: UUID) -> str:
        """Create a JWT refresh token."""
        expire = datetime.now(timezone.utc) + timedelta(
            days=self.settings.jwt_refresh_token_expire_days
        )
        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(
            payload,
            self.settings.jwt_secret_key,
            algorithm=self.settings.jwt_algorithm,
        )

    def decode_token(self, token: str) -> Optional[dict]:
        """Decode and validate a JWT token."""
        try:
            payload = jwt.decode(
                token,
                self.settings.jwt_secret_key,
                algorithms=[self.settings.jwt_algorithm],
            )
            return payload
        except JWTError:
            return None

    async def register_user(
        self,
        email: str,
        password: str,
        name: Optional[str] = None,
    ) -> dict:
        """Register a new user."""
        # Check if email exists
        if await UserRepository.email_exists(email):
            raise ValueError("Email already registered")

        # Hash password and create user
        password_hash = self.hash_password(password)
        user = await UserRepository.create(
            email=email,
            password_hash=password_hash,
            name=name,
        )

        if not user:
            raise ValueError("Failed to create user")

        # Generate tokens
        user_id = user["id"]
        access_token = self.create_access_token(user_id, email)
        refresh_token = self.create_refresh_token(user_id)

        return {
            "user": {
                "id": str(user_id),
                "email": user["email"],
                "name": user.get("name"),
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def authenticate_user(self, email: str, password: str) -> dict:
        """Authenticate user and return tokens."""
        user = await UserRepository.get_by_email(email)

        if not user:
            raise ValueError("Invalid email or password")

        if not user.get("password_hash"):
            raise ValueError("Invalid email or password")

        if not self.verify_password(password, user["password_hash"]):
            raise ValueError("Invalid email or password")

        # Generate tokens
        user_id = user["id"]
        access_token = self.create_access_token(user_id, email)
        refresh_token = self.create_refresh_token(user_id)

        return {
            "user": {
                "id": str(user_id),
                "email": user["email"],
                "name": user.get("name"),
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh_access_token(self, refresh_token: str) -> dict:
        """Generate new access token from refresh token."""
        payload = self.decode_token(refresh_token)

        if not payload:
            raise ValueError("Invalid refresh token")

        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")

        user_id = UUID(payload["sub"])
        user = await UserRepository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        access_token = self.create_access_token(user_id, user["email"])

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    async def get_user_from_token(self, token: str) -> Optional[dict]:
        """Get user from access token."""
        payload = self.decode_token(token)

        if not payload:
            return None

        if payload.get("type") != "access":
            return None

        user_id = UUID(payload["sub"])
        return await UserRepository.get_by_id(user_id)


# Singleton instance
_auth_service: Optional[AuthService] = None


def get_auth_service() -> AuthService:
    """Get auth service singleton."""
    global _auth_service
    if _auth_service is None:
        _auth_service = AuthService()
    return _auth_service
