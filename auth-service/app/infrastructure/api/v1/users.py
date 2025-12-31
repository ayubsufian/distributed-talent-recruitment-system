from fastapi import APIRouter, HTTPException, Depends, status
from app.application.user_use_cases import DeleteUserAccountUseCase
from app.infrastructure.security.jwt_handler import SecurityHandler
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
security_handler = SecurityHandler()


def get_delete_use_case(request):
    return request.app.state.delete_user_use_case


async def get_current_user_id(token: str = Depends(oauth2_scheme)):
    payload = security_handler.decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload.get("id")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: str,
    current_user_id: str = Depends(get_current_user_id),
    delete_uc: DeleteUserAccountUseCase = Depends(get_delete_use_case),
):
    """
    Delete a user account.
    Security Check: Users can only delete themselves (unless Admin logic is added).
    """
    if id != current_user_id:
        # In a real scenario, check if current_user is ADMIN here
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this account"
        )

    success = await delete_uc.execute(id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return None
