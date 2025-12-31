from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/", status_code=200)
async def health_check():
    """
    Standard Health Check.
    Used by Nginx and Docker Compose to verify service availability.
    """
    return {
        "status": "healthy",
        "service": "app-service",
        "timestamp": datetime.utcnow().isoformat(),
    }
