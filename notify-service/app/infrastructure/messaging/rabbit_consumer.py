import json
import aio_pika
import asyncio
from app.application.notify_use_cases import ProcessEventUseCase, AuditLogUseCase
from app.system.dlq_handler import DeadLetterQueueHandler
from app.system.audit_logger import SystemAuditLogger
from app.application.interfaces.repository import INotificationRepository


class MultiExchangeConsumer:
    def __init__(
        self,
        connection_url: str,
        process_use_case: ProcessEventUseCase,
        audit_use_case: AuditLogUseCase,
        repo: INotificationRepository,  # <--- Inject Repo
    ):
        self.connection_url = connection_url
        self.process_use_case = process_use_case
        self.audit_use_case = audit_use_case
        # Initialize DLQ Handler with Repo
        self.dlq_handler = DeadLetterQueueHandler(repo)
        self.connection = None

    async def start(self):
        self.connection = await aio_pika.connect_robust(self.connection_url)
        channel = await self.connection.channel()

        # 1. Declare Exchanges (Idempotent)
        exchanges = ["user_events", "job_events", "app_events"]
        declared_exchanges = []
        for exc_name in exchanges:
            exc = await channel.declare_exchange(
                exc_name, aio_pika.ExchangeType.TOPIC, durable=True
            )
            declared_exchanges.append(exc)

        # 2. Declare Single Queue for Notifications
        queue = await channel.declare_queue("notify_service_queue", durable=True)

        # 3. Bind Queue to ALL Exchanges
        for exc in declared_exchanges:
            await queue.bind(exc, routing_key="#")

        # 4. Process Messages
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        body = message.body.decode()
                        data = json.loads(body)
                        event_type = data.get("event", "unknown")

                        # A. System Audit (Log Everything)
                        SystemAuditLogger.log_event(event_type, data)
                        await self.audit_use_case.execute(
                            service_origin=message.exchange,
                            event_type=event_type,
                            payload=data,
                        )

                        # B. Business Logic (Send Notifications)
                        await self.process_use_case.execute(event_type, data)

                    except Exception as e:
                        # Pass exchange name as origin
                        await self.dlq_handler.handle_failure(
                            message.body, e, origin=message.exchange
                        )
