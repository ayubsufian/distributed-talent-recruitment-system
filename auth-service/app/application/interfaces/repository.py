from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models import User


class IUserRepository(ABC):
    """
    Interface for User Data Persistence.
    """

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email address."""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Retrieve a user by their ID."""
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        """Create or Update a user."""
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """Permanently remove a user."""
        pass
