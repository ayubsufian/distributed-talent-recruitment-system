from abc import ABC, abstractmethod
from app.domain.models import Application


class IAppEventPublisher(ABC):
    """
    Interface for publishing Application-related events to the Message Broker.
    """

    @abstractmethod
    async def publish_application_submitted(self, app: Application) -> None:
        """
        Publishes 'application.submitted' event.
        Subscribers: Notification Service (alerts recruiter).
        """
        pass

    @abstractmethod
    async def publish_status_changed(
        self, app_id: str, status: str, candidate_id: str
    ) -> None:
        """
        Publishes 'status.updated' event.
        Subscribers: Notification Service (alerts candidate).
        """
        pass
