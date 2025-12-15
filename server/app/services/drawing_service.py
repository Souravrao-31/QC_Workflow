from uuid import UUID
from sqlalchemy.orm import Session

from app.models.enums import UserRole, DrawingStatus
from app.models.drawing import Drawing
from app.repositories.drawing_repository import DrawingRepository
from app.services.workflow import WORKFLOW_TRANSITIONS
from app.services.exceptions import (
    PermissionDenied,
    InvalidStateTransition,
    DrawingAlreadyClaimed,
    NotOwner,
)

class DrawingService:

    @staticmethod
    def perform_action(
        db: Session,
        drawing: Drawing,
        user_id: UUID,
        user_role: UserRole,
        action: str,
    ):
        current_state = DrawingStatus(drawing.status)

        #  Validate action exists
        if action not in WORKFLOW_TRANSITIONS.get(current_state, {}):
            raise InvalidStateTransition(
                f"Action {action} not allowed from {current_state}"
            )

        rule = WORKFLOW_TRANSITIONS[current_state][action]

        #  Validate role
        if user_role != rule["role"]:
            raise PermissionDenied("Role not allowed")

        # CLAIM action (locking)
        if action == "CLAIM":
            success = DrawingRepository.claim_drawing(
                db=db,
                drawing_id=drawing.id,
                user_id=user_id,
                expected_status=current_state,
            )
            if not success:
                raise DrawingAlreadyClaimed()
            return

        # Ownership check for SUBMIT / APPROVE
        if drawing.assigned_to != user_id:
            raise NotOwner("Only current assignee can perform this action")

        # 5️⃣ Transition state
        drawing.status = rule["next"].value

        #  Release lock if required
        if not rule["lock"]:
            drawing.assigned_to = None
            drawing.locked_at = None

        db.commit()

