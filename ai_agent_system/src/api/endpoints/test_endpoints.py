"""Test endpoints for debugging and verification."""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/public")
async def test_public() -> Dict[str, Any]:
    """Test endpoint that doesn't require authentication."""
    return {
        "status": "ok",
        "message": "This is a public endpoint (no auth required)"
    }


@router.post("/token-info")
async def token_info(token: str) -> Dict[str, Any]:
    """Debug endpoint to analyze a token."""
    import jwt as pyjwt
    import json
    
    try:
        # Decode without verification to see the contents
        parts = token.split('.')
        if len(parts) != 3:
            return {
                "valid": False,
                "error": f"Token has {len(parts)} parts, should have 3"
            }
        
        # Decode header
        import base64
        header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
        
        return {
            "valid": True,
            "header": header,
            "payload": payload,
            "token_length": len(token)
        }
    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }
