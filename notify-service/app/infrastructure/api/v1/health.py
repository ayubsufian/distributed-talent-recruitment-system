from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/", status_code=200)
async def health_check():
    return {
        "status": "healthy",
        "service": "notify-service",
        "timestamp": datetime.utcnow().isoformat(),
    }
