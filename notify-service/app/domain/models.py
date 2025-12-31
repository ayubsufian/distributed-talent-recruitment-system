from enum import Enum
from typing import Optional, Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class NotificationType(str, Enum):
    EMAIL = "email"
    SYSTEM = "system"


class Notification(BaseModel):
    """
    Entity representing a user alert.
    """

    id: Optional[str] = None
    user_id: str
    message: str
    type: NotificationType
    read_status: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AuditEntry(BaseModel):
    """
    Entity representing a system audit log.
    """

    id: Optional[str] = None
    service_origin: str
    event_type: str
    payload: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# --- NEW MODEL ---
class FailedEvent(BaseModel):
    """
    Entity representing a message that failed processing (DLQ).
    """

    id: Optional[str] = None
    service_origin: str  # e.g., "job-service" or exchange name
    error_message: str
    raw_payload: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    resolved: bool = False


class NotificationResponse(BaseModel):
    id: str
    message: str
    read_status: bool
    created_at: datetime

    class Config:
        from_attributes = True
