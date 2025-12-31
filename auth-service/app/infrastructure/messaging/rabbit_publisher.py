import json
import aio_pika
from app.application.interfaces.messenger import IIdentityEventPublisher


class RabbitMQPublisher(IIdentityEventPublisher):
    def __init__(self, connection_url: str):
        self.connection_url = connection_url
        self.connection = None
        self.channel = None
        self.exchange = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.connection_url)
        self.channel = await self.connection.channel()
        # Declare a Topic Exchange
        self.exchange = await self.channel.declare_exchange(
            "user_events", aio_pika.ExchangeType.TOPIC, durable=True
        )

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def _publish(self, routing_key: str, message: dict):
        if not self.exchange:
            await self.connect()

        await self.exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=routing_key,
        )

    async def publish_user_deleted(self, user_id: str) -> None:
        payload = {"user_id": user_id, "event": "user.deleted"}
        await self._publish("user.deleted", payload)

    async def publish_user_registered(self, user_id: str, email: str) -> None:
        payload = {"user_id": user_id, "email": email, "event": "user.registered"}
        await self._publish("user.registered", payload)
