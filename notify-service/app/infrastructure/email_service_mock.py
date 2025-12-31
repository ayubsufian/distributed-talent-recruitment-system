from app.application.interfaces.email_service import IEmailService


class MockEmailService(IEmailService):
    async def send_email(self, recipient_id: str, subject: str, body: str) -> bool:
        print(f"--- [MOCK EMAIL SENT] ---")
        print(f"To: {recipient_id}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        print(f"-------------------------")
        return True
