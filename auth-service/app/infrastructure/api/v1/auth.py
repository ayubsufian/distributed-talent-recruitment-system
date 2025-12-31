from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.domain.models import UserCreate, UserResponse
from app.application.auth_use_cases import RegisterUserUseCase, LoginUserUseCase
from app.infrastructure.security.jwt_handler import SecurityHandler

# Dependencies (Injected from main.py or via Depends)
# For simplicity in this snippet, we assume these are passed or available via request state
# In a full app, we would use a proper Dependency Injection container or FastAPI Depends

router = APIRouter()


def get_auth_use_cases(request):
    # Helper to retrieve initialized use cases from app state
    return request.app.state.register_use_case, request.app.state.login_use_case


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(user_in: UserCreate, deps: tuple = Depends(get_auth_use_cases)):
    register_uc, _ = deps
    try:
        user = await register_uc.execute(user_in)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    deps: tuple = Depends(get_auth_use_cases),
):
    _, login_uc = deps

    # Note: form_data.username is mapped to email in our system
    user = await login_uc.execute(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate Token
    security = SecurityHandler()
    access_token = security.create_access_token(
        data={"sub": user.email, "id": user.id, "role": user.role}
    )

    return {"access_token": access_token, "token_type": "bearer"}
