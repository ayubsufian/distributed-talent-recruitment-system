from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import Application


class IApplicationRepository(ABC):
    """
    Interface for Application Data Persistence.
    """

    @abstractmethod
    async def save(self, app: Application) -> Application:
        """Create or Update an application."""
        pass

    @abstractmethod
    async def get_by_id(self, app_id: str) -> Optional[Application]:
        """Retrieve an application by its ID."""
        pass

    @abstractmethod
    async def get_by_job(self, job_id: str) -> List[Application]:
        """Retrieve all applications for a specific job."""
        pass

    @abstractmethod
    async def get_by_candidate(self, candidate_id: str) -> List[Application]:
        """Retrieve all applications submitted by a specific candidate."""
        pass

    @abstractmethod
    async def delete(self, app_id: str) -> bool:
        """Delete a single application."""
        pass

    @abstractmethod
    async def delete_by_job(self, job_id: str) -> int:
        """Delete all applications associated with a job ID."""
        pass

    @abstractmethod
    async def delete_by_candidate(self, candidate_id: str) -> int:
        """Delete all applications associated with a candidate ID."""
        pass
