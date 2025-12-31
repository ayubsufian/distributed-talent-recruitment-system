from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ApplicationStatus(str, Enum):
    PENDING = "Pending"
    REVIEWED = "Reviewed"
    SHORTLISTED = "Shortlisted"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"


class Application(BaseModel):
    """
    Internal Domain Entity representing a Job Application.
    """

    id: Optional[str] = None
    job_id: str
    candidate_id: str
    status: ApplicationStatus = ApplicationStatus.PENDING
    resume_file_id: str  # Reference to the file in GridFS
    applied_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ApplicationCreate(BaseModel):
    """
    DTO for initial submission metadata.
    Note: The actual file content is handled separately in the Use Case.
    """

    job_id: str


class ApplicationResponse(BaseModel):
    """
    DTO for returning application data.
    """

    id: str
    job_id: str
    candidate_id: str
    status: ApplicationStatus
    resume_file_id: str
    applied_at: datetime

    class Config:
        from_attributes = True
