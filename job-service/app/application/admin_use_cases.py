from app.application.interfaces.repository import IJobRepository
from app.application.interfaces.messenger import IJobEventPublisher


class ModeratorDeleteJobUseCase:
    def __init__(self, repo: IJobRepository, messenger: IJobEventPublisher):
        self.repo = repo
        self.messenger = messenger

    async def execute(self, job_id: str) -> bool:
        """
        Admin Only: Forceful removal of a job listing.
        """
        # 1. Check existence
        job = await self.repo.get_by_id(job_id)
        if not job:
            return False

        # 2. Delete from DB
        success = await self.repo.delete(job_id)

        # 3. Publish Event (Important: App Service needs to know to cancel applications)
        if success:
            await self.messenger.publish_job_deleted(job_id)

        return success
