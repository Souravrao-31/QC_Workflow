import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Drawing(Base):
    __tablename__ = "drawings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)

    status = Column(String, nullable=False)

    assigned_to = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True
    )
    
    assigned_user = relationship(
        "User",
        backref="assigned_drawings",
        lazy="joined",
    )

    locked_at = Column(DateTime(timezone=True), nullable=True)

    version = Column(Integer, default=1)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
