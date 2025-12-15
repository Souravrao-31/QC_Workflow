from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import LoginRequest, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        token = AuthService.login(
            db, request.email, request.password
        )
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"access_token": token}
