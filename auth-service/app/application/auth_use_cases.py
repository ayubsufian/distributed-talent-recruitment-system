from typing import Optional
from app.domain.models import User, UserCreate, UserRole
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
            raise ValueError("User with this email already exists")

        # 2. Hash the password
        hashed_pw = self.password_manager.get_password_hash(user_in.password)

        # 3. Create User Entity
        new_user = User(
            email=user_in.email, hashed_password=hashed_pw, role=user_in.role
        )

        # 4. Save to Repository
        saved_user = await self.repo.save(new_user)

        # 5. Publish Event (Optional based on requirements, but good practice)
        if saved_user.id:
            await self.messenger.publish_user_registered(
                saved_user.id, saved_user.email
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

        # 2. Verify Password
        if not self.password_manager.verify_password(password, user.hashed_password):
            return None

        # 3. Check if active
        if not user.is_active:
            raise ValueError("User account is inactive")

        return user
