from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.utils.auth import create_access_token, hash_password, verify_password, api_key_store

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/token", response_model=TokenResponse, summary="Get JWT access token")
async def login(payload: LoginRequest) -> TokenResponse:
    # Placeholder: replace with real user validation
    if payload.username == "demo" and payload.password == "demo":
        token = create_access_token({"sub": payload.username, "scopes": ["read", "write"]})
        return TokenResponse(access_token=token)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


@router.get("/validate", summary="Validate current API key/token")
async def validate() -> dict[str, str]:
    return {"status": "valid"}
