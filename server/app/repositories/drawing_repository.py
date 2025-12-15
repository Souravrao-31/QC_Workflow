from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import text


class DrawingRepository:
    """
    Repository layer for Drawing-related DB operations.
    All DB access related to drawings should live here.
    """

    @staticmethod
    def claim_drawing(
        db: Session,
        drawing_id: UUID,
        user_id: UUID,
        expected_status: str,
    ) -> bool:
        """
        Atomically claim a drawing.

        - Only succeeds if:
            - drawing exists
            - drawing is in expected_status
            - drawing is NOT already assigned

        Returns:
            True  -> claim successful
            False -> already claimed / invalid state
        """

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
                "drawing_id": drawing_id,
                "user_id": user_id,
                "expected_status": expected_status,
            },
        )

        return result.fetchone() is not None
