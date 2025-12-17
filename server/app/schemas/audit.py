from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    id: UUID
    action: str
    from_status: str | None
    to_status: str | None
    user_role: str
    created_at: datetime

    drawing_id: UUID
    drawing_title: str

    user_id: UUID
    user_name: str

    class Config:
        from_attributes = True
