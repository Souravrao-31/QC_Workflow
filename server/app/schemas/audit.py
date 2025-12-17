from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class AuditLogResponse(BaseModel):
    id: UUID
    drawing_id: UUID
    user_id: UUID
    user_role: str
    action: str
    from_status: str | None
    to_status: str | None
    created_at: datetime

    class Config:
        from_attributes = True
