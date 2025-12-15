from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    DRAFTER = "DRAFTER"
    SHIFT_LEAD = "SHIFT_LEAD"
    FINAL_QC = "FINAL_QC"


class DrawingStatus(str, Enum):
    UNASSIGNED = "UNASSIGNED"
    DRAFTING = "DRAFTING"
    FIRST_QC = "FIRST_QC"
    FINAL_QC = "FINAL_QC"
    APPROVED = "APPROVED"
