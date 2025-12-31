from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    ACTIVE = "Active"
    ARCHIVED = "Archived"
    CLOSED = "Closed"
    FLAGGED = "Flagged"  # For admin moderation


class Job(BaseModel):
    """
    Internal Domain Entity representing a Job Posting.
    """

    id: Optional[str] = None
    recruiter_id: str
    title: str
    description: str
    location: str
    salary_range: Optional[str] = None
    status: JobStatus = JobStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class JobCreate(BaseModel):
    """
    DTO for creating a new job.
    """

    title: str
    description: str
    location: str
    salary_range: Optional[str] = None


class JobResponse(BaseModel):
    """
    DTO for returning job data to the client.
    """

    id: str
    recruiter_id: str
    title: str
    description: str
    location: str
    salary_range: Optional[str]
    status: JobStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
