from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
    Form,
    Request,
)
from fastapi.responses import StreamingResponse
from typing import List
from app.domain.models import ApplicationResponse, ApplicationCreate
from app.application.app_use_cases import SubmitApplicationUseCase
from app.application.interfaces.repository import IApplicationRepository
from app.application.interfaces.file_store import IFileStore
from app.infrastructure.api.auth_deps import get_current_user

router = APIRouter()


def get_submit_use_case(request: Request):
    return request.app.state.submit_use_case


def get_repo(request: Request):
    return request.app.state.app_repo


def get_file_store(request: Request):
    return request.app.state.file_store


# --- FIX: Path changed to "" ---
@router.post(
    "", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED
)
async def submit_application(
    job_id: str = Form(...),
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    use_case: SubmitApplicationUseCase = Depends(get_submit_use_case),
):
    candidate_id = current_user.get("id")
    role = current_user.get("role")
    if role != "Candidate":
        raise HTTPException(status_code=403, detail="Only candidates can apply")
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    content = await file.read()
    app_in = ApplicationCreate(job_id=job_id)
    return await use_case.execute(
        app_in, candidate_id, file.filename, content, file.content_type
    )


@router.get("/me", response_model=List[ApplicationResponse])
async def get_my_applications(
    current_user: dict = Depends(get_current_user),
    repo: IApplicationRepository = Depends(get_repo),
):
    return await repo.get_by_candidate(current_user.get("id"))


@router.get("/{id}/resume")
async def get_resume(
    id: str,
    current_user: dict = Depends(get_current_user),
    repo: IApplicationRepository = Depends(get_repo),
    file_store: IFileStore = Depends(get_file_store),
):
    app = await repo.get_by_id(id)
    if not app:
        raise HTTPException(status_code=404)
    grid_out = await file_store.download_file(app.resume_file_id)
    return StreamingResponse(grid_out, media_type="application/pdf")
