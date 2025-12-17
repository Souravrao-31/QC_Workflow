from uuid import UUID
from sqlalchemy.orm import Session

from app.models.enums import UserRole, DrawingStatus
from app.models.drawing import Drawing
from app.repositories.drawing_repository import DrawingRepository
from app.schemas.drawing import DrawingResponse
from app.services.workflow import WORKFLOW_TRANSITIONS
from app.services.exceptions import (
    PermissionDenied,
    InvalidStateTransition,
    DrawingAlreadyClaimed,
    NotOwner,
)
from app.core.dependencies import CurrentUser
from app.repositories.audit_repository import AuditRepository

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

        if current_state == DrawingStatus.APPROVED:
            raise InvalidStateTransition(
                "No actions are allowed on an approved drawing"
            )

        # Validate action
        if action not in WORKFLOW_TRANSITIONS.get(current_state, {}):
            raise InvalidStateTransition(
                f"Action '{action}' is not allowed when drawing is in '{current_state.value}' state"
            )

        rule = WORKFLOW_TRANSITIONS[current_state][action]

        # Validate role
        if user_role != rule["role"]:
            raise PermissionDenied("Role not allowed")

        # CLAIM (atomic)
        if action == "CLAIM":
            success = DrawingRepository.claim_drawing(
                db=db,
                drawing_id=UUID(str(drawing.id)),
                user_id=user_id,
                expected_status=current_state.value,
            )
            if not success:
                raise DrawingAlreadyClaimed()

            db.commit()
            db.expire_all()
            return

        # Refresh after possible raw SQL
        db.refresh(drawing)

        # Ownership check
        if action in {"SUBMIT", "APPROVE"}:
            if str(drawing.assigned_to) != str(user_id):
                raise NotOwner("Only current assignee can perform this action")

        # Transition
        drawing.status = rule["next"].value

        # Release lock if needed
        if not rule["lock"]:
            drawing.assigned_to = None
            drawing.locked_at = None

        db.commit()



    @staticmethod
    def list_drawings_for_user(
        db: Session,
        user: CurrentUser,
    ):
        role = user.role
        user_id = user.id

        if role == UserRole.ADMIN:
            drawings = DrawingRepository.list_unassigned(db)

        elif role == UserRole.DRAFTER:
            drawings = (
                DrawingRepository.list_drafting_unclaimed(db)
                + DrawingRepository.list_assigned_to_user(db, user_id)
            )

        elif role == UserRole.SHIFT_LEAD:
            drawings = (
                DrawingRepository.list_first_qc_unclaimed(db)
                + DrawingRepository.list_assigned_to_user(db, user_id)
            )

        elif role == UserRole.FINAL_QC:
            drawings = (
                DrawingRepository.list_final_qc_unclaimed(db)
                + DrawingRepository.list_assigned_to_user(db, user_id)
            )

        else:
            drawings = []

        # Remove duplicates
        unique = {d.id: d for d in drawings}.values()
        return DrawingService._to_response(unique)

    @staticmethod
    def get_my_drawings(
        db: Session,
        user_id: UUID,
    ):
        drawings = DrawingRepository.list_assigned_to_user(db, user_id)
        return DrawingService._to_response(drawings)



    @staticmethod
    def _to_response(drawings):
        return [
            DrawingResponse(
                id=d.id,
                title=d.title,
                status=d.status,
                assigned_to=d.assigned_to,
                assigned_to_name=(
                    d.assigned_user.name if d.assigned_user else None
                ),
                created_at=d.created_at,
            )
            for d in drawings
        ]



    @staticmethod
    def release(
        db: Session,
        drawing: Drawing,
        user_id: UUID,
    ):
        success = DrawingRepository.release_drawing(
            db=db,
            drawing_id=UUID(str(drawing.id)),
            user_id=user_id,
        )

        if not success:
            raise NotOwner("You do not own this drawing")

        db.commit()
