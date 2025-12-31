import os
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from datetime import datetime

# Infrastructure
from app.infrastructure.database.mongo_repo import MongoUserRepository
from app.infrastructure.messaging.rabbit_publisher import RabbitMQPublisher
from app.infrastructure.security.jwt_handler import SecurityHandler
from app.infrastructure.api.v1 import auth, users

# Use Cases
from app.application.auth_use_cases import RegisterUserUseCase, LoginUserUseCase
from app.application.user_use_cases import DeleteUserAccountUseCase

# Config - Pulling from .env via Docker Compose
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
RABBITMQ_URI = os.getenv("RABBITMQ_URI", "amqp://guest:guest@localhost:5672/")
# NEW: Get the specific DB name for this service
DB_NAME = os.getenv("DATABASE_NAME", "auth_db")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize Database with the dynamic DB_NAME
    mongo_client = AsyncIOMotorClient(MONGO_URI)
    user_repo = MongoUserRepository(mongo_client, DB_NAME)  # <--- UPDATED THIS LINE

    # 2. Initialize Messaging
    publisher = RabbitMQPublisher(RABBITMQ_URI)
    await publisher.connect()

    # 3. Initialize Security
    security = SecurityHandler()

    # 4. Initialize Use Cases (Dependency Injection)
    app.state.register_use_case = RegisterUserUseCase(user_repo, security, publisher)
    app.state.login_use_case = LoginUserUseCase(user_repo, security)
    app.state.delete_user_use_case = DeleteUserAccountUseCase(user_repo, publisher)

    yield

    # Cleanup
    await publisher.close()
    mongo_client.close()


app = FastAPI(title="Auth Service", lifespan=lifespan)

# Register Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "auth-service",
        "timestamp": datetime.utcnow().isoformat(),
    }
