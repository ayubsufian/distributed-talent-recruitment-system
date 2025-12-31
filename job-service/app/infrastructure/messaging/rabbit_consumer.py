import json
import aio_pika
import asyncio
from app.application.job_use_cases import HandleUserDeletedUseCase


class RabbitMQConsumer:
    def __init__(
        self, connection_url: str, handle_user_deleted: HandleUserDeletedUseCase
    ):
        self.connection_url = connection_url
        self.handle_user_deleted = handle_user_deleted
        self.connection = None

    async def start(self):
        self.connection = await aio_pika.connect_robust(self.connection_url)
        channel = await self.connection.channel()

        # Declare the exchange we want to listen to (defined by Auth Service)
        user_exchange = await channel.declare_exchange(
            "user_events", aio_pika.ExchangeType.TOPIC, durable=True
        )

        # Declare a queue for this service
        queue = await channel.declare_queue("job_service_user_events", durable=True)

        # Bind queue to exchange for specific routing key
        await queue.bind(user_exchange, routing_key="user.deleted")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = json.loads(message.body.decode())
                    event_type = data.get("event")

                    if event_type == "user.deleted":
                        user_id = data.get("user_id")
                        if user_id:
                            print(f"[JobService] Processing user.deleted for {user_id}")
                            await self.handle_user_deleted.execute(user_id)
