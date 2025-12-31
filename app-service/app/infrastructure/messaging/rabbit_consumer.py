import json
import aio_pika
import asyncio
from app.application.app_use_cases import HandleJobDeletedCleanupUseCase
from app.application.interfaces.repository import IApplicationRepository
from app.application.interfaces.file_store import IFileStore


class RabbitMQConsumer:
    def __init__(
        self,
        connection_url: str,
        cleanup_use_case: HandleJobDeletedCleanupUseCase,
        repo: IApplicationRepository,  # Injected for direct candidate cleanup if needed
        file_store: IFileStore,
    ):
        self.connection_url = connection_url
        self.cleanup_use_case = cleanup_use_case
        self.repo = repo
        self.file_store = file_store
        self.connection = None

    async def start(self):
        self.connection = await aio_pika.connect_robust(self.connection_url)
        channel = await self.connection.channel()

        # 1. Declare Exchanges (Idempotent)
        job_exchange = await channel.declare_exchange(
            "job_events", aio_pika.ExchangeType.TOPIC, durable=True
        )
        user_exchange = await channel.declare_exchange(
            "user_events", aio_pika.ExchangeType.TOPIC, durable=True
        )

        # 2. Declare Queue
        queue = await channel.declare_queue("app_service_cleanup_queue", durable=True)

        # 3. Bind Queue to Exchanges
        await queue.bind(job_exchange, routing_key="job.deleted")
        await queue.bind(user_exchange, routing_key="user.deleted")

        # 4. Process Messages
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = json.loads(message.body.decode())
                    event = data.get("event")

                    if event == "job.deleted":
                        job_id = data.get("job_id")
                        if job_id:
                            print(f"[AppService] Cleaning up apps for job {job_id}")
                            await self.cleanup_use_case.execute(job_id)

                    elif event == "user.deleted":
                        user_id = data.get("user_id")
                        if user_id:
                            print(
                                f"[AppService] Cleaning up apps for candidate {user_id}"
                            )
                            # Logic to clean up candidate applications
                            # Note: Ideally this would be a separate Use Case, but implementing inline for brevity
                            apps = await self.repo.get_by_candidate(user_id)
                            for app in apps:
                                if app.resume_file_id:
                                    await self.file_store.delete_file(
                                        app.resume_file_id
                                    )
                            await self.repo.delete_by_candidate(user_id)
