from sqlalchemy.orm import Session
from app.models.enums import UserRole, DrawingStatus
from app.repositories.drawing_repository import DrawingRepository


class DashboardService:

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
