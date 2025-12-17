from sqlalchemy.orm import Session
from uuid import UUID
from app.models.audit import AuditLog


class AuditRepository:

    @staticmethod
    def create(
        db: Session,
        drawing_id: UUID,
        user_id: UUID,
        action: str,
        from_status: str,
        to_status: str,
        user_role: str,
    ):
        log = AuditLog(
            drawing_id=drawing_id,
            user_id=user_id,
            action=action,
            from_status=from_status,
            to_status=to_status,
            user_role=user_role,
        )
        db.add(log)
