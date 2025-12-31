from abc import ABC, abstractmethod


class IPasswordManager(ABC):
    """Interface for password hashing and verification."""

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass

    @abstractmethod
    def get_password_hash(self, password: str) -> str:
        pass
