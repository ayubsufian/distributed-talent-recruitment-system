from abc import ABC, abstractmethod


class IEmailService(ABC):
    @abstractmethod
    async def send_email(self, recipient_id: str, subject: str, body: str) -> bool:
        """
        Sends an email.
        recipient_id is used to look up email (or passed directly if payload has it).
        """
        pass
