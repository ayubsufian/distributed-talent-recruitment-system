from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.domain.models import UserCreate, UserResponse
from app.application.auth_use_cases import RegisterUserUseCase, LoginUserUseCase
from app.infrastructure.security.jwt_handler import SecurityHandler

router = APIRouter()


# Dependency Helper: Retrieves use cases from the FastAPI app state
def get_auth_use_cases(request: Request):
    return request.app.state.register_use_case, request.app.state.login_use_case


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    user_in: UserCreate,
    deps: tuple = Depends(get_auth_use_cases),
):
    register_uc, _ = deps
    try:
        user = await register_uc.execute(user_in)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(
    # --- FIXED: Use Annotated for strict OAuth2 form handling ---
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    deps: Annotated[tuple, Depends(get_auth_use_cases)],
):
    _, login_uc = deps

    # Attempt to authenticate
    user = await login_uc.execute(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Initialize Security Handler to generate JWT
    security = SecurityHandler()

    # User ID must be converted to string for the JWT payload
    access_token = security.create_access_token(
        data={"sub": user.email, "id": str(user.id), "role": user.role}
    )

    return {"access_token": access_token, "token_type": "bearer"}
