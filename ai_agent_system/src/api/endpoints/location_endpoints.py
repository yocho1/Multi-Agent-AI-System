"""Location detection endpoints for user profile."""

from fastapi import APIRouter, Request
from typing import Optional

router = APIRouter(prefix="/api/v1", tags=["location"])


@router.get("/location")
async def detect_location(request: Request) -> dict:
    """
    Detect user location from their IP address.
    This endpoint is called by the frontend to get the user's location.
    """
    try:
        # Get client IP from request
        client_ip = request.client.host
        
        # For localhost/127.0.0.1, return a default location
        if client_ip in ("127.0.0.1", "localhost", "::1"):
            return {
                "location": "Local Development",
                "ip": client_ip,
                "source": "local"
            }
        
        # Try to get location from IP using a backend service
        # We'll use a simple implementation that queries ipapi.co
        import httpx
        
        async with httpx.AsyncClient() as client:
            try:
                # Use ipapi.co with the client's IP
                response = await client.get(
                    f"https://ipapi.co/{client_ip}/json/",
                    timeout=5.0
                )
                if response.status_code == 200:
                    data = response.json()
                    city = data.get("city")
                    region = data.get("region")
                    location = f"{city}, {region}" if (city and region) else data.get("country_name", "Unknown Location")
                    
                    return {
                        "location": location,
                        "ip": client_ip,
                        "source": "ip_geolocation",
                        "city": city,
                        "region": region,
                        "country": data.get("country_name")
                    }
            except Exception as e:
                print(f"Failed to get location from ipapi.co: {e}")
        
        # If all else fails, return unknown
        return {
            "location": None,
            "ip": client_ip,
            "source": "unknown"
        }
        
    except Exception as e:
        return {
            "location": None,
            "error": str(e),
            "source": "error"
        }
