from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.drawing import Drawing
from app.models.enums import DrawingStatus


class DrawingRepository:

    # WRITE OPERATIONS (CONCURRENCY) handle racing events
   

    @staticmethod
    def claim_drawing(
        db: Session,
        drawing_id: UUID,
        user_id: UUID,
        expected_status: str,
    ) -> bool:
        result = db.execute(
            text(
                """
                UPDATE drawings
                SET assigned_to = :user_id,
                    locked_at = now()
                WHERE id = :drawing_id
                  AND status = :expected_status
                  AND assigned_to IS NULL
                RETURNING id
                """
            ),
            {
                "drawing_id": str(drawing_id),
                "user_id": str(user_id),
                "expected_status": expected_status,
            },
        )

        row = result.fetchone()

        if row:
            db.commit()  
            return True

        db.rollback()
        return False


#Read

    @staticmethod
    def get_all(db: Session):
        return db.query(Drawing).all()

    @staticmethod
    def get_assigned_to_user(
        db: Session,
        user_id: UUID,
    ):
        """Get drawings assigned to current user"""
        return (
            db.query(Drawing)
            .filter(Drawing.assigned_to == user_id)
            .all()
        )

    @staticmethod
    def get_available_for_status(
        db: Session,
        status: DrawingStatus,
    ):
        """Get unassigned drawings for a given workflow state"""
        return (
            db.query(Drawing)
            .filter(
                Drawing.status == status.value,
                Drawing.assigned_to.is_(None),
            )
            .all()
        )
    
          
          
    @staticmethod
    def release_drawing(
            db: Session,
            drawing_id: UUID,
            user_id: UUID,
    ) -> bool:
        """
        Release a drawing lock.

        Only succeeds if:
        - drawing is assigned to user_id
        """

        result = db.execute(
            text(
                """
                UPDATE drawings
                SET assigned_to = NULL,
                    locked_at = NULL
                WHERE id = :drawing_id
                AND assigned_to = :user_id
                RETURNING id
                """
            ),
            {
                "drawing_id": drawing_id,
                "user_id": user_id,
            },
        )

        return result.fetchone() is not None