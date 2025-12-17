from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class DrawingResponse(BaseModel):
    id: UUID
    title: str
    status: str
    assigned_to: Optional[UUID]
    assigned_to_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
