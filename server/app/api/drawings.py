from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.models.drawing import Drawing
from app.schemas.drawing_action import DrawingActionRequest
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
    # hardcoded user (we’ll replace with auth later)
    user_id: UUID = Depends(lambda: UUID("00")),
    user_role: str = Depends(lambda: "SHIFT_LEAD"),
):
    drawing = get_drawing_or_404(db, drawing_id)

    try:
        DrawingService.perform_action(
            db=db,
            drawing=drawing,
            user_id=user_id,
            user_role=user_role,
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
