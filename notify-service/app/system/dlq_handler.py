import logging
from app.application.interfaces.repository import INotificationRepository
from app.domain.models import FailedEvent

logger = logging.getLogger("DLQHandler")


class DeadLetterQueueHandler:
    """
    Handles messages that failed processing by persisting them to the database.
    """

    def __init__(self, repo: INotificationRepository):
        self.repo = repo

    async def handle_failure(
        self, message_body: bytes, error: Exception, origin: str = "unknown"
    ):
        try:
            payload_str = message_body.decode()
        except:
            payload_str = str(message_body)

        logger.error(f"CRITICAL: Message processing failed. Error: {str(error)}")

        # Persist to DB
        event = FailedEvent(
            service_origin=origin, error_message=str(error), raw_payload=payload_str
        )
        await self.repo.save_failed_event(event)
