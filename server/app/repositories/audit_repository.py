from sqlalchemy.orm import Session
from app.models.audit import AuditLog


class AuditRepository:
    @staticmethod
    def create(
        db: Session,
        *,
        drawing_id,
        user_id,
        user_role,
        action,
        from_status,
        to_status,
    ):
        log = AuditLog(
            drawing_id=drawing_id,
            user_id=user_id,
            user_role=user_role,
            action=action,
            from_status=from_status,
            to_status=to_status,
        )
        db.add(log)
