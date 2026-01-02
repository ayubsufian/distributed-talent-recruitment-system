from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserRole(str, Enum):
    ADMIN = "Admin"
    RECRUITER = "Recruiter"
    CANDIDATE = "Candidate"


class User(BaseModel):
    """
    Internal Domain Entity.
    """

    id: Optional[str] = None
    email: EmailStr
    hashed_password: str
    role: UserRole
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Allow mapping from database dictionaries
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class UserCreate(BaseModel):
    """
    DTO for User Registration inputs.
    """

    email: EmailStr
    password: str
    role: UserRole = UserRole.CANDIDATE

    # Hardening: Strip spaces, ignore extra fields (like confirmPassword),
    # and ensure role matches the Enum value.
    model_config = ConfigDict(
        str_strip_whitespace=True, use_enum_values=True, extra="ignore"
    )


class UserResponse(BaseModel):
    """
    DTO for User Responses (No passwords).
    """

    id: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime

    # Ensures that the database 'id' field is mapped correctly
    model_config = ConfigDict(from_attributes=True)
