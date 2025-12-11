"""Authentication middleware for protecting routes with Firebase."""
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from src.utils.firebase_auth import get_firebase_auth
from src.config.logging_config import get_logger

logger = get_logger(module=__name__)

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Optional[dict]:
    """
    Dependency to get current authenticated user from Firebase token.
    
    Args:
        credentials: HTTP Authorization credentials
        
    Returns:
        Dict with user information if authenticated
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    if not credentials:
        logger.warning("No credentials provided")
        raise HTTPException(
            status_code=401,
            detail="Missing authentication token"
        )
    
    token = credentials.credentials
    logger.debug(f"Verifying token, length: {len(token)}, first 50 chars: {token[:50]}")
    
    try:
        firebase_auth = get_firebase_auth()
        user_info = await firebase_auth.verify_token(token)
        
        if not user_info:
            logger.warning("Token verification returned None")
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )
        
        logger.info(f"✓ User authenticated: {user_info.get('email')}")
        return user_info
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication error ({type(e).__name__}): {str(e)}")
        raise HTTPException(
            status_code=401,
            detail="Authentication failed"
        )


async def require_auth(request: Request):
    """
    Middleware to require authentication for routes.
    
    Args:
        request: FastAPI request object
        
    Raises:
        HTTPException: If authentication fails
    """
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        raise HTTPException(
            status_code=401,
            detail="Missing authentication token"
        )
    
    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication scheme"
        )
    
    token = auth_header.replace("Bearer ", "")
    firebase_auth = get_firebase_auth()
    
    user_info = await firebase_auth.verify_token(token)
    
    if not user_info:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    # Attach user info to request state
    request.state.user = user_info


def optional_auth(request: Request) -> Optional[dict]:
    """
    Optional authentication - doesn't raise error if no token.
    
    Args:
        request: FastAPI request object
        
    Returns:
        User info if authenticated, None otherwise
    """
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    
    token = auth_header.replace("Bearer ", "")
    firebase_auth = get_firebase_auth()
    
    try:
        user_info = firebase_auth.verify_token(token)
        return user_info
    except Exception:
        return None
