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


