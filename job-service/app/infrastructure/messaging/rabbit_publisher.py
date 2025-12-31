import json
import aio_pika
from app.domain.models import Job
from app.application.interfaces.messenger import IJobEventPublisher


class RabbitMQPublisher(IJobEventPublisher):
    def __init__(self, connection_url: str):
        self.connection_url = connection_url
        self.connection = None
        self.channel = None
        self.exchange = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.connection_url)
        self.channel = await self.connection.channel()
        # Declare Topic Exchange for Job events
        self.exchange = await self.channel.declare_exchange(
            "job_events", aio_pika.ExchangeType.TOPIC, durable=True
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

    async def publish_job_posted(self, job: Job) -> None:
        payload = job.dict()
        payload["event"] = "job.posted"
        await self._publish("job.posted", payload)

    async def publish_job_deleted(self, job_id: str) -> None:
        payload = {"job_id": job_id, "event": "job.deleted"}
        await self._publish("job.deleted", payload)
