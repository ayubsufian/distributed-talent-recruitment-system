from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from typing import List

from app.domain.models import ApplicationResponse, ApplicationCreate
from app.application.app_use_cases import SubmitApplicationUseCase
from app.application.interfaces.repository import IApplicationRepository
from app.application.interfaces.file_store import IFileStore
from app.infrastructure.api.auth_deps import get_current_user

router = APIRouter()


# Dependency Helpers
def get_submit_use_case(request):
    return request.app.state.submit_use_case


def get_repo(request):
    return request.app.state.app_repo


def get_file_store(request):
    return request.app.state.file_store


@router.post(
    "/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED
)
async def submit_application(
    job_id: str = Form(...),
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    use_case: SubmitApplicationUseCase = Depends(get_submit_use_case),
):
    """
    Submit a new application with a Resume PDF.
    """
    candidate_id = current_user.get("id")
    role = current_user.get("role")

    if role != "Candidate":
        raise HTTPException(status_code=403, detail="Only candidates can apply")

    # Validate File Type
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Read file content
    content = await file.read()

    app_in = ApplicationCreate(job_id=job_id)

    return await use_case.execute(
        app_in=app_in,
        candidate_id=candidate_id,
        file_filename=file.filename,
        file_content=content,
        content_type=file.content_type,
    )


@router.get("/{id}/resume")
async def get_resume(
    id: str,
    current_user: dict = Depends(get_current_user),
    repo: IApplicationRepository = Depends(get_repo),
    file_store: IFileStore = Depends(get_file_store),
):
    """
    Stream the resume PDF.
    Security: Only the Candidate who applied or a Recruiter can view.
    """
    app = await repo.get_by_id(id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    user_id = current_user.get("id")
    role = current_user.get("role")

    # RBAC Check
    if role == "Candidate" and app.candidate_id != user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to view this resume"
        )

    # Download Stream
    grid_out = await file_store.download_file(app.resume_file_id)
    if not grid_out:
        raise HTTPException(status_code=404, detail="Resume file not found")

    # Stream response
    return StreamingResponse(
        grid_out,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename={app.resume_file_id}.pdf"},
    )


@router.get("/me", response_model=List[ApplicationResponse])
async def get_my_applications(
    current_user: dict = Depends(get_current_user),
    repo: IApplicationRepository = Depends(get_repo),
):
    return await repo.get_by_candidate(current_user.get("id"))
