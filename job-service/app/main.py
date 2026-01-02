import os
import asyncio
from datetime import datetime
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager

# Infrastructure
from app.infrastructure.database.mongo_repo import MongoJobRepository
from app.infrastructure.messaging.rabbit_publisher import RabbitMQPublisher
from app.infrastructure.messaging.rabbit_consumer import RabbitMQConsumer
from app.infrastructure.api.v1 import jobs

# Use Cases
from app.application.job_use_cases import (
    CreateJobUseCase,
    GetJobsUseCase,
    GetJobDetailUseCase,
    HandleUserDeletedUseCase,
)
from app.application.admin_use_cases import ModeratorDeleteJobUseCase

# Config - Pulling from .env via Docker Compose
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
RABBITMQ_URI = os.getenv("RABBITMQ_URI", "amqp://guest:guest@localhost:5672/")
# NEW: Get the specific DB name for this service
DB_NAME = os.getenv("DATABASE_NAME", "job_db")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize Database with the dynamic DB_NAME
    mongo_client = AsyncIOMotorClient(MONGO_URI)
    job_repo = MongoJobRepository(mongo_client, DB_NAME)  # <--- UPDATED

    # 2. Initialize Publisher
    publisher = RabbitMQPublisher(RABBITMQ_URI)
    await publisher.connect()

    # 3. Initialize Use Cases
    app.state.create_job_use_case = CreateJobUseCase(job_repo, publisher)
    app.state.get_jobs_use_case = GetJobsUseCase(job_repo)
    app.state.get_job_detail_use_case = GetJobDetailUseCase(job_repo)
    app.state.admin_delete_job_use_case = ModeratorDeleteJobUseCase(job_repo, publisher)

    # 4. Initialize Consumer (Background Task)
    # Note: Because job_repo is already initialized with DB_NAME,
    # the consumer will automatically delete jobs from the correct DB.
    handle_user_deleted = HandleUserDeletedUseCase(job_repo)
    consumer = RabbitMQConsumer(RABBITMQ_URI, handle_user_deleted)

    # Run consumer in background
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


app = FastAPI(title="Job Service", lifespan=lifespan)

# FIX: Add the prefix here. This combines with the "" in jobs.py
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])


@app.get("/jobs/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "job-service",
        "timestamp": datetime.utcnow().isoformat(),
    }
