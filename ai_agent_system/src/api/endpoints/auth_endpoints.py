"""Authentication endpoints for Firebase."""
from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel, EmailStr
from typing import Optional

from src.utils.firebase_auth import get_firebase_auth
from src.config.logging_config import get_logger

logger = get_logger(module=__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])


class TokenRequest(BaseModel):
    """Request model for token verification."""
    token: str


class UserResponse(BaseModel):
    """Response model for user information."""
    uid: str
    email: Optional[str] = None
    email_verified: bool = False
    name: Optional[str] = None
    picture: Optional[str] = None


class CustomTokenRequest(BaseModel):
    """Request model for custom token creation."""
    uid: str
    claims: Optional[dict] = None


@router.post("/verify", response_model=UserResponse)
async def verify_token(request: TokenRequest):
    """
    Verify Firebase ID token.
    
    Args:
        request: TokenRequest with ID token
        
    Returns:
        UserResponse with user information
        
    Raises:
        HTTPException: If token is invalid
    """
    firebase_auth = get_firebase_auth()
    
    user_info = await firebase_auth.verify_token(request.token)
    
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return UserResponse(**user_info)


@router.get("/user/{uid}", response_model=UserResponse)
async def get_user(
    uid: str,
    authorization: Optional[str] = Header(None)
):
    """
    Get user information by UID.
    
    Args:
        uid: Firebase user ID
        authorization: Bearer token (optional, for auth check)
        
    Returns:
        UserResponse with user information
        
    Raises:
        HTTPException: If user not found or unauthorized
    """
    # If authorization header provided, verify it
    if authorization:
        token = authorization.replace("Bearer ", "")
        firebase_auth = get_firebase_auth()
        current_user = await firebase_auth.verify_token(token)
        
        if not current_user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        # Users can only get their own info unless they have admin claims
        if current_user['uid'] != uid:
            raise HTTPException(status_code=403, detail="Forbidden")
    
    firebase_auth = get_firebase_auth()
    user_info = await firebase_auth.get_user(uid)
    
    if not user_info:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        uid=user_info['uid'],
        email=user_info['email'],
        email_verified=user_info['email_verified'],
        name=user_info['display_name'],
        picture=user_info['photo_url'],
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user(authorization: str = Header(...)):
    """
    Get current authenticated user information.
    
    Args:
        authorization: Bearer token from request header
        
    Returns:
        UserResponse with user information
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = authorization.replace("Bearer ", "")
    firebase_auth = get_firebase_auth()
    
    user_info = await firebase_auth.verify_token(token)
    
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return UserResponse(**user_info)


@router.post("/custom-token")
async def create_custom_token(
    request: CustomTokenRequest,
    authorization: str = Header(...)
):
    """
    Create a custom token for a user (admin only).
    
    Args:
        request: CustomTokenRequest with UID and optional claims
        authorization: Bearer token (must be admin)
        
    Returns:
        Dict with custom token
        
    Raises:
        HTTPException: If unauthorized or token creation fails
    """
    # Verify admin token
    token = authorization.replace("Bearer ", "")
    firebase_auth = get_firebase_auth()
    current_user = await firebase_auth.verify_token(token)
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    # Create custom token
    custom_token = await firebase_auth.create_custom_token(
        request.uid,
        request.claims
    )
    
    if not custom_token:
        raise HTTPException(status_code=500, detail="Failed to create custom token")
    
    return {
        "custom_token": custom_token,
        "uid": request.uid,
    }
