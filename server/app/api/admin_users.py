from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, CurrentUser
from app.schemas.user import CreateUserRequest, UserResponse
from app.services.user_service import UserService
from app.services.exceptions import PermissionDenied

router = APIRouter(prefix="/admin/users", tags=["Admin"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    request: CreateUserRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    try:
        user = UserService.create_user(
            db=db,
            name=request.name,
            password=request.password,
            role=request.role,
            current_user_role=current_user.role,
        )
    except PermissionDenied as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return user
