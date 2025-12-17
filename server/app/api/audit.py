from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, CurrentUser
from app.models.audit import AuditLog
from app.schemas.audit import AuditLogResponse

router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get("", response_model=list[AuditLogResponse])
def list_audit_logs(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    q = db.query(AuditLog)

    if current_user.role != "ADMIN":
        q = q.filter(AuditLog.user_id == current_user.id)

    logs = (
        q.order_by(AuditLog.created_at.desc())
        .limit(200)
        .all()
    )
    return [
        AuditLogResponse(
            id=l.id,
            action=l.action,
            from_status=l.from_status,
            to_status=l.to_status,
            user_role=l.user_role,
            created_at=l.created_at,
            drawing_id=l.drawing_id,
            drawing_title=l.drawing.title,
            user_id=l.user_id,
            user_name=l.user.name,
        )
        for l in logs
    ]

