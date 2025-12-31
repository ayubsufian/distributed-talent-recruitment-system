from typing import List
from app.domain.models import Application, ApplicationCreate, ApplicationStatus
from app.application.interfaces.repository import IApplicationRepository
from app.application.interfaces.file_store import IFileStore


class SubmitApplicationUseCase:
    def __init__(self, repo: IApplicationRepository, file_store: IFileStore):
        self.repo = repo
        self.file_store = file_store

    async def execute(
        self,
        app_in: ApplicationCreate,
        candidate_id: str,
        file_filename: str,
        file_content: bytes,
        content_type: str,
    ) -> Application:
        """
        Orchestrates the Resume Upload and Metadata Creation.
        """
        # 1. Upload Resume to File Store (GridFS)
        file_id = await self.file_store.upload_file(
            filename=file_filename, content=file_content, content_type=content_type
        )

        # 2. Create Application Entity
        new_app = Application(
            job_id=app_in.job_id,
            candidate_id=candidate_id,
            resume_file_id=file_id,
            status=ApplicationStatus.PENDING,
        )

        # 3. Save Metadata to Repository
        saved_app = await self.repo.save(new_app)

        return saved_app


class HandleJobDeletedCleanupUseCase:
    """
    Subscriber Logic:
    Listens for 'job.deleted' events.
    Ensures no orphaned PDF files remain in storage when a job is removed.
    """

    def __init__(self, repo: IApplicationRepository, file_store: IFileStore):
        self.repo = repo
        self.file_store = file_store

    async def execute(self, job_id: str) -> int:
        # 1. Retrieve all applications for this job
        applications = await self.repo.get_by_job(job_id)

        if not applications:
            return 0

        # 2. Delete associated Resume PDFs from File Store
        for app in applications:
            if app.resume_file_id:
                await self.file_store.delete_file(app.resume_file_id)

        # 3. Delete Application records from Repository
        deleted_count = await self.repo.delete_by_job(job_id)

        return deleted_count
