from app.domain.models import Notification, NotificationType, AuditEntry
from app.application.interfaces.repository import INotificationRepository
from app.application.interfaces.email_service import IEmailService


class AuditLogUseCase:
    def __init__(self, repo: INotificationRepository):
        self.repo = repo

    async def execute(self, service_origin: str, event_type: str, payload: dict):
        entry = AuditEntry(
            service_origin=service_origin, event_type=event_type, payload=payload
        )
        await self.repo.save_audit_log(entry)


class ProcessEventUseCase:
    """
    Core logic: Maps technical events to user notifications.
    """

    def __init__(self, repo: INotificationRepository, email_service: IEmailService):
        self.repo = repo
        self.email_service = email_service

    async def execute(self, event_type: str, payload: dict):
        # 1. Map Event to Notification Logic
        if event_type == "user.registered":
            # Welcome Email
            user_id = payload.get("user_id")
            email = payload.get("email")
            message = "Welcome to the Recruitment Platform!"

            # Send Email
            await self.email_service.send_email(email, "Welcome!", message)

            # Save System Alert
            await self._create_alert(user_id, message)

        elif event_type == "application.submitted":
            # Notify Recruiter (assuming job payload has recruiter_id, or we fetch it)
            # For this demo, we assume payload has 'recruiter_id' or we skip
            recruiter_id = payload.get("recruiter_id")  # Hypothetical field
            if recruiter_id:
                msg = f"New application received for Job {payload.get('job_id')}"
                await self._create_alert(recruiter_id, msg)

        elif event_type == "job.posted":
            # In a real system, this would query matching candidates.
            # Here we just log that we processed it.
            pass

    async def _create_alert(self, user_id: str, message: str):
        note = Notification(
            user_id=user_id, message=message, type=NotificationType.SYSTEM
        )
        await self.repo.save_notification(note)


class GetUserNotificationsUseCase:
    def __init__(self, repo: INotificationRepository):
        self.repo = repo

    async def execute(self, user_id: str) -> list[Notification]:
        return await self.repo.get_by_user(user_id)


class MarkNotificationReadUseCase:
    def __init__(self, repo: INotificationRepository):
        self.repo = repo

    async def execute(self, notification_id: str) -> bool:
        return await self.repo.mark_as_read(notification_id)
