from abc import ABC, abstractmethod


class IIdentityEventPublisher(ABC):
    """
    Interface for publishing Identity/Auth related events to the Message Broker.
    """

    @abstractmethod
    async def publish_user_deleted(self, user_id: str) -> None:
        """
        Publishes the 'user.deleted' event to trigger cascading deletes
        in Job, App, and Notify services.
        """
        pass

    @abstractmethod
    async def publish_user_registered(self, user_id: str, email: str) -> None:
        """
        Publishes the 'user.registered' event (e.g., for Welcome Emails).
        """
        pass
