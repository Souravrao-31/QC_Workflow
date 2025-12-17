import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    drawing_id = Column(
        UUID(as_uuid=True),
        ForeignKey("drawings.id"),
        nullable=False,
        index=True,
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    user_role = Column(String, nullable=False)

    action = Column(String, nullable=False)  

    from_status = Column(String, nullable=True)
    to_status = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
