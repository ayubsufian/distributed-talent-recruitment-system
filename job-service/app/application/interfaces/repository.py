from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import Job


class IJobRepository(ABC):
    """
    Interface for Job Data Persistence.
    """

    @abstractmethod
    async def save(self, job: Job) -> Job:
        """Create or Update a job."""
        pass

    @abstractmethod
    async def get_by_id(self, job_id: str) -> Optional[Job]:
        """Retrieve a job by its ID."""
        pass

    @abstractmethod
    async def get_all(self, limit: int = 10, offset: int = 0) -> List[Job]:
        """Retrieve a paginated list of jobs."""
        pass

    @abstractmethod
    async def search(self, query: str) -> List[Job]:
        """Search jobs by title or description."""
        pass

    @abstractmethod
    async def delete(self, job_id: str) -> bool:
        """Delete a specific job."""
        pass

    @abstractmethod
    async def delete_by_recruiter(self, recruiter_id: str) -> int:
        """
        Delete all jobs belonging to a specific recruiter.
        Used for cascading deletes when a user is removed.
        Returns the number of deleted documents.
        """
        pass
