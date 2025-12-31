from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.domain.models import JobResponse, JobCreate
from app.application.job_use_cases import (
    CreateJobUseCase,
    GetJobsUseCase,
    GetJobDetailUseCase,
)
from app.application.admin_use_cases import ModeratorDeleteJobUseCase
from app.infrastructure.api.auth_deps import require_recruiter, require_admin

router = APIRouter()


# Dependency Helpers
def get_create_use_case(request):
    return request.app.state.create_job_use_case


def get_list_use_case(request):
    return request.app.state.get_jobs_use_case


def get_detail_use_case(request):
    return request.app.state.get_job_detail_use_case


def get_admin_delete_use_case(request):
    return request.app.state.admin_delete_job_use_case


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_in: JobCreate,
    recruiter_id: str = Depends(require_recruiter),
    use_case: CreateJobUseCase = Depends(get_create_use_case),
):
    return await use_case.execute(job_in, recruiter_id)


@router.get("/", response_model=List[JobResponse])
async def list_jobs(
    q: Optional[str] = None,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    use_case: GetJobsUseCase = Depends(get_list_use_case),
):
    return await use_case.execute(query=q, limit=limit, offset=offset)


@router.get("/{id}", response_model=JobResponse)
async def get_job(
    id: str, use_case: GetJobDetailUseCase = Depends(get_detail_use_case)
):
    job = await use_case.execute(id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.delete("/{id}/admin", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_job(
    id: str,
    _: dict = Depends(require_admin),
    use_case: ModeratorDeleteJobUseCase = Depends(get_admin_delete_use_case),
):
    success = await use_case.execute(id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    return None
