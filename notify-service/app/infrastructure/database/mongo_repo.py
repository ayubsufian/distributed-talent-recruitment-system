from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from app.domain.models import Notification, AuditEntry, FailedEvent
from app.application.interfaces.repository import INotificationRepository


class MongoNotificationRepository(INotificationRepository):

    def __init__(self, client: AsyncIOMotorClient, db_name: str):
        self.db = client[db_name]
        self.notifications = self.db["notifications"]
        self.audit_logs = self.db["audit_logs"]
        self.failed_events = self.db["failed_events"]  # <--- New Collection

    def _map_note(self, doc):
        if not doc:
            return None
        doc["id"] = str(doc["_id"])
        return Notification(**doc)

    def _map_failed(self, doc):
        if not doc:
            return None
        doc["id"] = str(doc["_id"])
        return FailedEvent(**doc)

    async def save_notification(self, notification: Notification) -> Notification:
        data = notification.dict(exclude={"id"})
        result = await self.notifications.insert_one(data)
        notification.id = str(result.inserted_id)
        return notification

    async def get_by_user(self, user_id: str, limit: int = 20) -> List[Notification]:
        cursor = (
            self.notifications.find({"user_id": user_id})
            .sort("created_at", -1)
            .limit(limit)
        )
        return [self._map_note(doc) async for doc in cursor]

    async def mark_as_read(self, notification_id: str) -> bool:
        try:
            oid = ObjectId(notification_id)
        except:
            return False
        res = await self.notifications.update_one(
            {"_id": oid}, {"$set": {"read_status": True}}
        )
        return res.modified_count > 0

    async def save_audit_log(self, entry: AuditEntry) -> AuditEntry:
        data = entry.dict(exclude={"id"})
        result = await self.audit_logs.insert_one(data)
        entry.id = str(result.inserted_id)
        return entry

    # --- NEW IMPLEMENTATIONS ---
    async def save_failed_event(self, event: FailedEvent) -> FailedEvent:
        data = event.dict(exclude={"id"})
        result = await self.failed_events.insert_one(data)
        event.id = str(result.inserted_id)
        return event

    async def get_failed_events(self, limit: int = 50) -> List[FailedEvent]:
        cursor = self.failed_events.find().sort("timestamp", -1).limit(limit)
        return [self._map_failed(doc) async for doc in cursor]
