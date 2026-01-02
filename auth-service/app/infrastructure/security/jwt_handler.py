import os
import bcrypt  # <--- Using the direct library
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from app.application.interfaces.security import IPasswordManager

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET", "yeigr732hr7hhf4fbrf7")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class SecurityHandler(IPasswordManager):
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plain password against the stored hash using the bcrypt library directly.
        """
        try:
            # Bcrypt requires bytes for comparison
            return bcrypt.checkpw(
                plain_password.encode("utf-8"), hashed_password.encode("utf-8")
            )
        except Exception:
            return False

    def get_password_hash(self, password: str) -> str:
        """
        Generates a secure hash from a plain text password.
        """
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        # Convert bytes back to string for storage in MongoDB
        return hashed.decode("utf-8")

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """Generates a JWT Access Token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def decode_access_token(self, token: str) -> Optional[dict]:
        """Decodes and validates a JWT Access Token."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None
