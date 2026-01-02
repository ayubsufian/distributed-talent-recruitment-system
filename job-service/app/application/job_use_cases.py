from typing import List, Optional
from app.domain.models import Job, JobCreate, JobStatus
from app.application.interfaces.repository import IJobRepository
from app.application.interfaces.messenger import IJobEventPublisher


class CreateJobUseCase:
    def __init__(self, repo: IJobRepository, messenger: IJobEventPublisher):
        self.repo = repo
        self.messenger = messenger

    async def execute(self, job_in: JobCreate, recruiter_id: str) -> Job:
        # 1. Create Entity
        new_job = Job(
            recruiter_id=recruiter_id,
            title=job_in.title,
            description=job_in.description,
            location=job_in.location,
            salary_range=job_in.salary_range,
            status=JobStatus.ACTIVE,
        )

        # 2. Save to DB
        saved_job = await self.repo.save(new_job)

        # 3. Publish Event (Triggers notifications)
        if saved_job.id:
            await self.messenger.publish_job_posted(saved_job)

        return saved_job


class GetJobsUseCase:
    def __init__(self, repo: IJobRepository):
        self.repo = repo

    async def execute(
        self, query: Optional[str] = None, limit: int = 10, offset: int = 0
    ) -> List[Job]:
        if query:
            return await self.repo.search(query)
        return await self.repo.get_all(limit, offset)


class GetJobDetailUseCase:
    def __init__(self, repo: IJobRepository):
        self.repo = repo

    async def execute(self, job_id: str) -> Optional[Job]:
        return await self.repo.get_by_id(job_id)


class HandleUserDeletedUseCase:
    """
    Subscriber Logic:
    Listens for 'user.deleted' events from Auth Service.
    """

    def __init__(self, repo: IJobRepository):
        self.repo = repo

    async def execute(self, recruiter_id: str) -> int:
        # Cascading delete: Remove all jobs posted by this user
        deleted_count = await self.repo.delete_by_recruiter(recruiter_id)
        return deleted_count
