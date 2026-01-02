from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.domain.models import NotificationResponse
from app.application.notify_use_cases import (
    GetUserNotificationsUseCase,
    MarkNotificationReadUseCase,
)


async def get_current_user_id():
    return "user_123_placeholder"


router = APIRouter()


def get_fetch_use_case(request: Request):
    return request.app.state.get_notes_use_case


def get_mark_use_case(request: Request):
    return request.app.state.mark_read_use_case


# --- FIX: Matches /notifications exactly ---
@router.get("", response_model=List[NotificationResponse])
async def get_my_notifications(
    user_id: str = Depends(get_current_user_id),
    use_case: GetUserNotificationsUseCase = Depends(get_fetch_use_case),
):
    return await use_case.execute(user_id)


@router.patch("/{id}/read", status_code=status.HTTP_204_NO_CONTENT)
async def mark_as_read(
    id: str, use_case: MarkNotificationReadUseCase = Depends(get_mark_use_case)
):
    success = await use_case.execute(id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    return None
