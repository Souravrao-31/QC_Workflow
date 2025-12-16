from pydantic import BaseModel
from enum import Enum


class DrawingAction(str, Enum):
    ASSIGN = "ASSIGN"
    CLAIM = "CLAIM"
    SUBMIT = "SUBMIT"
    APPROVE = "APPROVE"


class DrawingActionRequest(BaseModel):
    action: DrawingAction
