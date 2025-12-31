import os
import asyncio
from datetime import datetime
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager

# Infrastructure
from app.infrastructure.database.mongo_repo import MongoNotificationRepository
from app.infrastructure.email_service_mock import MockEmailService
from app.infrastructure.messaging.rabbit_consumer import MultiExchangeConsumer
from app.infrastructure.api.v1 import alerts, system  # <--- Import system router

# Use Cases
from app.application.notify_use_cases import (
    ProcessEventUseCase,
    AuditLogUseCase,
    GetUserNotificationsUseCase,
    MarkNotificationReadUseCase,
)

# Config - Pulling from .env via Docker Compose
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
RABBITMQ_URI = os.getenv("RABBITMQ_URI", "amqp://guest:guest@localhost:5672/")
# NEW: Get the specific DB name for this service (defaulting to notify_db)
DB_NAME = os.getenv("DATABASE_NAME", "notify_db")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Init DB with the dynamic DB_NAME
    mongo_client = AsyncIOMotorClient(MONGO_URI)
    repo = MongoNotificationRepository(mongo_client, DB_NAME)

    # Store repo in state for API access
    app.state.repo = repo

    # 2. Init Services
    email_service = MockEmailService()

    # 3. Init Use Cases
    process_uc = ProcessEventUseCase(repo, email_service)
    audit_uc = AuditLogUseCase(repo)

    app.state.get_notes_use_case = GetUserNotificationsUseCase(repo)
    app.state.mark_read_use_case = MarkNotificationReadUseCase(repo)

    # 4. Start Background Consumer (Injecting Repo now)
    consumer = MultiExchangeConsumer(RABBITMQ_URI, process_uc, audit_uc, repo)
    task = asyncio.create_task(consumer.start())

    yield

    # Cleanup
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    mongo_client.close()


app = FastAPI(title="Notification Service", lifespan=lifespan)

app.include_router(alerts.router, prefix="/notifications", tags=["Notifications"])
app.include_router(
    system.router, prefix="/system", tags=["System"]
)  # <--- Register System Router


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "notify-service",
        "timestamp": datetime.utcnow().isoformat(),
    }
