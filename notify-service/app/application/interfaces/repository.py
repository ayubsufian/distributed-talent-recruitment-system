from abc import ABC, abstractmethod
from typing import List
from app.domain.models import Notification, AuditEntry, FailedEvent


class INotificationRepository(ABC):
    @abstractmethod
    async def save_notification(self, notification: Notification) -> Notification:
        pass

    @abstractmethod
    async def get_by_user(self, user_id: str, limit: int = 20) -> List[Notification]:
        pass

    @abstractmethod
    async def mark_as_read(self, notification_id: str) -> bool:
        pass

    @abstractmethod
    async def save_audit_log(self, entry: AuditEntry) -> AuditEntry:
        pass

    # --- NEW METHODS ---
    @abstractmethod
    async def save_failed_event(self, event: FailedEvent) -> FailedEvent:
        pass

    @abstractmethod
    async def get_failed_events(self, limit: int = 50) -> List[FailedEvent]:
        pass
