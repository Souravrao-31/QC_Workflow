from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import get_current_user, CurrentUser
from app.models.drawing import Drawing
from app.schemas.drawing_action import DrawingActionRequest
from app.schemas.drawing import DrawingResponse
from app.services.drawing_service import DrawingService
from app.services.exceptions import (
    PermissionDenied,
    InvalidStateTransition,
    DrawingAlreadyClaimed,
    NotOwner,
)

router = APIRouter(prefix="/drawings", tags=["Drawings"])


def get_drawing_or_404(
    db: Session,
    drawing_id: UUID,
) -> Drawing:
    drawing = db.query(Drawing).filter(Drawing.id == drawing_id).first()
    if not drawing:
        raise HTTPException(status_code=404, detail="Drawing not found")
    return drawing


@router.post("/{drawing_id}/actions")
def perform_drawing_action(
    drawing_id: UUID,
    request: DrawingActionRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    drawing = get_drawing_or_404(db, drawing_id)

    try:
        DrawingService.perform_action(
            db=db,
            drawing=drawing,
            user_id=current_user.id,
            user_role=current_user.role,
            action=request.action.value,
        )
    except PermissionDenied as e:
        raise HTTPException(status_code=403, detail=str(e))
    except NotOwner as e:
        raise HTTPException(status_code=403, detail=str(e))
    except DrawingAlreadyClaimed:
        raise HTTPException(
            status_code=409,
            detail="Drawing already claimed by another user",
        )
    except InvalidStateTransition as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"status": "success"}


@router.get("", response_model=list[DrawingResponse])
def list_all_drawings(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Forbidden")

    return DrawingService.get_all_drawings(db, current_user.role)


@router.get("/me", response_model=list[DrawingResponse])
def my_drawings(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return DrawingService.get_my_drawings(db, current_user.id)


@router.get("/available", response_model=list[DrawingResponse])
def available_drawings(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return DrawingService.get_available_drawings(db, current_user.role)
