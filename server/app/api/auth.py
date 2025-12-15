from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import LoginRequest, Token
from app.services.auth_service import AuthService
from app.services.exceptions import InvalidCredentials

router = APIRouter(prefix="/auth", tags=["Auth"])



@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    try:
        access_token = AuthService.login(
            db=db,
            name=request.name,
            password=request.password,
        )
    except InvalidCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid name or password",
        )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
