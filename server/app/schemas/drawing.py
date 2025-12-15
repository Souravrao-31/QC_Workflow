from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class DrawingResponse(BaseModel):
    id: UUID
    title: str
    status: str
    assigned_to: Optional[UUID]
    created_at: datetime

    class Config:
        from_attributes = True
