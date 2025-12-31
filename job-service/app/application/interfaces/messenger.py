from abc import ABC, abstractmethod
from app.domain.models import Job


class IJobEventPublisher(ABC):
    """
    Interface for publishing Job-related events to the Message Broker.
    """

    @abstractmethod
    async def publish_job_posted(self, job: Job) -> None:
        """
        Publishes 'job.posted' event.
        Subscribers: Notification Service (alerts candidates).
        """
        pass

    @abstractmethod
    async def publish_job_deleted(self, job_id: str) -> None:
        """
        Publishes 'job.deleted' event.
        Subscribers: App Service (cancels applications), Notify Service.
        """
        pass
