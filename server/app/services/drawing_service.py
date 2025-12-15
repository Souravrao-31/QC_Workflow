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
        
    
    @staticmethod
    def get_all_drawings(db: Session, role: UserRole):
        if role != UserRole.ADMIN:
            raise PermissionError("Only admin can view all drawings")
        return DrawingRepository.get_all(db)
    @staticmethod
    def get_my_drawings(db: Session, user_id):
        return DrawingRepository.get_assigned_to_user(db, user_id)

    @staticmethod
    def get_available_drawings(db: Session, role: UserRole):
        role_status_map = {
            UserRole.DRAFTER: DrawingStatus.DRAFTING,
            UserRole.SHIFT_LEAD: DrawingStatus.FIRST_QC,
            UserRole.FINAL_QC: DrawingStatus.FINAL_QC,
        }

        if role not in role_status_map:
            return []

        return DrawingRepository.get_available_for_status(
            db,
            role_status_map[role],
        )
        
    @staticmethod
    def release(
        db: Session,
        drawing: Drawing,
        user_id: UUID,
    ):
        success = DrawingRepository.release_drawing(
            db=db,
            drawing_id=drawing.id,
            user_id=user_id,
        )

        if not success:
            raise NotOwner("You do not own this drawing")

        db.commit()

