import json
import aio_pika
from app.domain.models import Application

# Assuming interface exists in application/interfaces/messenger.py
# If not, this class defines the contract implicitly for the infrastructure layer.


class RabbitMQPublisher:
    def __init__(self, connection_url: str):
        self.connection_url = connection_url
        self.connection = None
        self.channel = None
        self.exchange = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.connection_url)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            "app_events", aio_pika.ExchangeType.TOPIC, durable=True
        )

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def _publish(self, routing_key: str, message: dict):
        if not self.exchange:
            await self.connect()

        await self.exchange.publish(
            aio_pika.Message(
                body=json.dumps(message, default=str).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=routing_key,
        )

    async def publish_application_submitted(self, app: Application) -> None:
        payload = app.dict()
        payload["event"] = "application.submitted"
        await self._publish("application.submitted", payload)

    async def publish_status_updated(
        self, app_id: str, status: str, candidate_id: str
    ) -> None:
        payload = {
            "app_id": app_id,
            "status": status,
            "candidate_id": candidate_id,
            "event": "status.updated",
        }
        await self._publish("status.updated", payload)
