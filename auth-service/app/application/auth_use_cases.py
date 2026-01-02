from typing import Optional
from app.domain.models import User, UserCreate
from app.application.interfaces.repository import IUserRepository
from app.application.interfaces.security import IPasswordManager
from app.application.interfaces.messenger import IIdentityEventPublisher


class RegisterUserUseCase:
    def __init__(
        self,
        repo: IUserRepository,
        password_manager: IPasswordManager,
        messenger: IIdentityEventPublisher,
    ):
        self.repo = repo
        self.password_manager = password_manager
        self.messenger = messenger

    async def execute(self, user_in: UserCreate) -> User:
        # 1. Check if user already exists
        existing_user = await self.repo.get_by_email(user_in.email)
        if existing_user:
            # This triggers the 400 Bad Request in the router
            raise ValueError(f"Account with email {user_in.email} already exists")

        # 2. Hash the password (using the direct bcrypt implementation)
        hashed_pw = self.password_manager.get_password_hash(user_in.password)

        # 3. Create User Entity
        new_user = User(
            email=user_in.email, hashed_password=hashed_pw, role=user_in.role
        )

        # 4. Save to Repository
        saved_user = await self.repo.save(new_user)

        # 5. Publish Event (Now verified to exist in RabbitMQPublisher)
        if saved_user.id:
            await self.messenger.publish_user_registered(
                str(saved_user.id), saved_user.email  # Explicit string cast for safety
            )

        return saved_user


class LoginUserUseCase:
    def __init__(self, repo: IUserRepository, password_manager: IPasswordManager):
        self.repo = repo
        self.password_manager = password_manager

    async def execute(self, email: str, password: str) -> Optional[User]:
        # 1. Retrieve User
        user = await self.repo.get_by_email(email)
        if not user:
            return None

        # 2. Verify Password (using bcrypt.checkpw)
        if not self.password_manager.verify_password(password, user.hashed_password):
            return None

        # 3. Check if active
        if not user.is_active:
            raise ValueError("User account is inactive")

        return user
