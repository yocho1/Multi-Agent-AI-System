from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import bcrypt
import jwt

from src.config.settings import settings
from src.config.logging_config import get_logger

logger = get_logger(component="auth")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt (max 72 bytes)."""
    # Bcrypt has a 72-byte limit, truncate if needed
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    """Verify plain password against hash."""
    plain_bytes = plain.encode('utf-8')[:72]
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(plain_bytes, hashed_bytes)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(hours=24)
    )
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode JWT access token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.InvalidTokenError as exc:
        logger.warning("invalid token", error=str(exc))
        return None


class APIKeyStore:
    """In-memory API key store; replace with DB lookup in production."""

    def __init__(self) -> None:
        self.keys: Dict[str, Dict[str, Any]] = {
            "demo-key-12345": {"name": "demo", "active": True, "permissions": ["read", "write"]},
        }

    def validate_key(self, key: str) -> bool:
        """Check if API key is valid and active."""
        if key not in self.keys:
            return False
        return self.keys[key].get("active", False)

    def get_permissions(self, key: str) -> list[str]:
        """Get permissions for an API key."""
        if key not in self.keys:
            return []
        return self.keys[key].get("permissions", [])


api_key_store = APIKeyStore()
