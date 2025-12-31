from typing import List
from fastapi import APIRouter, Depends
from app.domain.models import FailedEvent
from app.application.interfaces.repository import INotificationRepository

router = APIRouter()


def get_repo(request):
    return request.app.state.repo


@router.get("/events/failed", response_model=List[FailedEvent])
async def get_failed_events(
    limit: int = 50, repo: INotificationRepository = Depends(get_repo)
):
    """
    View failed messages currently in the Dead Letter Queue (Persisted in DB).
    """
    return await repo.get_failed_events(limit)
