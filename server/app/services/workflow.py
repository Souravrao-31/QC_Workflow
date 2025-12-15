from app.models.enums import UserRole, DrawingStatus

WORKFLOW_TRANSITIONS = {
    DrawingStatus.UNASSIGNED: {
        "ASSIGN": {
            "role": UserRole.ADMIN,
            "next": DrawingStatus.DRAFTING,
            "lock": True,
        }
    },
    DrawingStatus.DRAFTING: {
        "CLAIM": {
            "role": UserRole.DRAFTER,
            "next": DrawingStatus.DRAFTING,
            "lock": True,
        },
        "SUBMIT": {
            "role": UserRole.DRAFTER,
            "next": DrawingStatus.FIRST_QC,
            "lock": False,
        },
    },
    DrawingStatus.FIRST_QC: {
        "CLAIM": {
            "role": UserRole.SHIFT_LEAD,
            "next": DrawingStatus.FIRST_QC,
            "lock": True,
        },
        "SUBMIT": {
            "role": UserRole.SHIFT_LEAD,
            "next": DrawingStatus.FINAL_QC,
            "lock": False,
        },
    },
    DrawingStatus.FINAL_QC: {
        "CLAIM": {
            "role": UserRole.FINAL_QC,
            "next": DrawingStatus.FINAL_QC,
            "lock": True,
        },
        "APPROVE": {
            "role": UserRole.FINAL_QC,
            "next": DrawingStatus.APPROVED,
            "lock": False,
        },
    },
}
