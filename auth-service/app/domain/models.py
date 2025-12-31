from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    ADMIN = "Admin"
    RECRUITER = "Recruiter"
    CANDIDATE = "Candidate"


class User(BaseModel):
    """
    Internal Domain Entity representing a User.
    """

    id: Optional[str] = None
    email: EmailStr
    hashed_password: str
    role: UserRole
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(BaseModel):
    """
    DTO for User Registration inputs.
    """

    email: EmailStr
    password: str
    role: UserRole = UserRole.CANDIDATE


class UserResponse(BaseModel):
    """
    DTO for User Responses (excludes sensitive data like passwords).
    """

    id: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
