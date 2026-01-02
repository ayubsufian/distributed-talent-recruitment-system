import os
import asyncio
from datetime import datetime
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from contextlib import asynccontextmanager

# Infrastructure
from app.infrastructure.database.mongo_repo import MongoApplicationRepository
from app.infrastructure.database.gridfs_store import GridFSFileStore
from app.infrastructure.messaging.rabbit_publisher import RabbitMQPublisher
from app.infrastructure.messaging.rabbit_consumer import RabbitMQConsumer
from app.infrastructure.api.v1 import apps

# Use Cases
from app.application.app_use_cases import (
    SubmitApplicationUseCase,
    HandleJobDeletedCleanupUseCase,
)

# Config - Pulling from .env via Docker Compose
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
RABBITMQ_URI = os.getenv("RABBITMQ_URI", "amqp://guest:guest@localhost:5672/")
# NEW: Get the specific DB name for this service (defaulting to app_db)
DB_NAME = os.getenv("DATABASE_NAME", "app_db")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize Database & GridFS with dynamic DB_NAME
    mongo_client = AsyncIOMotorClient(MONGO_URI)
    db = mongo_client[DB_NAME]  # <--- Uses the injected DB_NAME
    bucket = AsyncIOMotorGridFSBucket(db)

    # Initialize Repo and FileStore
    app_repo = MongoApplicationRepository(mongo_client, DB_NAME)  # <--- UPDATED
    file_store = GridFSFileStore(bucket)

    # 2. Initialize Publisher
    publisher = RabbitMQPublisher(RABBITMQ_URI)
    await publisher.connect()

    # 3. Initialize Use Cases
    app.state.submit_use_case = SubmitApplicationUseCase(app_repo, file_store)
    app.state.cleanup_use_case = HandleJobDeletedCleanupUseCase(app_repo, file_store)

    # Inject dependencies for API access
    app.state.app_repo = app_repo
    app.state.file_store = file_store

    # 4. Initialize Consumer (Background Task)
    consumer = RabbitMQConsumer(
        connection_url=RABBITMQ_URI,
        cleanup_use_case=app.state.cleanup_use_case,
        repo=app_repo,
        file_store=file_store,
    )
    task = asyncio.create_task(consumer.start())

    yield

    # Cleanup
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    await publisher.close()
    mongo_client.close()


app = FastAPI(title="Application Service", lifespan=lifespan)

# FIX: Add the prefix here. This combines with the "" in apps.py
app.include_router(apps.router, prefix="/applications", tags=["Applications"])


@app.get("/applications/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "app-service",
        "timestamp": datetime.utcnow().isoformat(),
    }
